#!usr/bin/python
#!-*- coding:utf-8 -*-
import math
import multiprocessing
import logging
logging.basicConfig(level=logging.DEBUG)



def unwrap_self_count_get_freq_w_e(arg, **kwarg):
    return SoaClass._subtask_get_w_label_freq(*arg, **kwarg)


def unwrap_self_f(arg, **kwarg):
    return SoaClass._subtask_func(*arg, **kwarg)


class SoaClass(object):
    def __init__(self, labeled_corpus, n_thread=1):
        assert isinstance(labeled_corpus, dict)
        assert isinstance(n_thread, int)

        self.n_thread = n_thread
        self.labeled_corpus = labeled_corpus

        self.label_list = self._make_label_list()
        self.vocabulary_list = self._make_vocabulary_list()
        self.labeled_document = self._conv_into_documnet()

        logging.debug(msg="Start counting total label frequency")
        # count total sentences having label
        self.total_sents = self._get_total_sentences()
        logging.debug(msg="Start counting total frequencies of word")
        # count total freq per words
        self.total_word_freq = self._get_total_word_freq()


        # for all label, ラベルeのsentences数を数えるメソッド freq(e) {label: freq}
        logging.debug(msg="Start counting freq_label")
        self.label_freq_dict = self._get_freq_label()
        # for all label, ラベルeのnot sentence数を数えるメソッド freq(not_e) {label: freq}
        logging.debug(msg="Start counting freq_not_label")

        self.label_freq_not_dict = self._get_freq_not_label()

        # for all words and label, 単語wがラベルeに出現した回数を数えるメソッド{word: {label: freq}}
        logging.debug(msg="Start counting freq_w_label")
        self.w_e_freq = self._get_w_label_freq(n_thread=n_thread)
        logging.debug(msg="Start counting freq_w_not_label")
        # for all words and label, 単語wがラベルe以外に出現した回数を数えるメソッド{word: {label: freq}}
        self.w_not_e_freq = self._get_w_not_label_freq()

        logging.debug(msg="Preprocessing Done")


    def _get_total_word_freq(self):
        """get total frequencies of words

        :return:
        """

        word_total_freq_dict = {}
        for word in self.vocabulary_list:
            word_total_freq = 0
            for doc_id, doc in self.labeled_document.items():
                word_total_freq += doc.count(word)

            word_total_freq_dict[word] = word_total_freq

        return word_total_freq_dict


    def _get_total_sentences(self):
        """get total sentences inside given dataset

        :return:
        """
        total_sents = 0
        for label in self.label_list:
             total_sents += len(self.labeled_corpus[label])

        return total_sents


    def _conv_into_documnet(self):
        """convert [[unicode]] into [unicode]

        :return:
        """

        labeled_documents = {}
        for label, list_array_2_dim in self.labeled_corpus.items():
            documents = [morph for sent in list_array_2_dim for morph in sent]
            labeled_documents[label] = documents

        return labeled_documents


    def _make_vocabulary_list(self):
        """make vocaburary list inside given data

        :return:
        """
        assert isinstance(self.labeled_corpus, dict)
        sentences_in_label = self.labeled_corpus.values()
        vocabulary = [
            base_morph
            for doc_in_label in sentences_in_label
            for sentence in doc_in_label
            for base_morph in sentence
        ]

        return set(vocabulary)


    def _make_label_list(self):
        """make label list inside given data

        :return:
        """
        assert isinstance(self.labeled_corpus, dict)
        return self.labeled_corpus.keys()


    def _get_freq_label(self):
        """count up frequencies of having labels

        :return:
        """
        label_freq_dict = {}
        for label in self.label_list:
            label_freq_dict[label] = len(self.labeled_corpus[label])

        return label_freq_dict


    def _get_freq_not_label(self):
        """count up frequencies of NOT having labels

        :return:
        """
        label_freq_not_e = {}
        for label in self.label_list:
            n_not_e = self.total_sents - self.label_freq_dict[label]
            label_freq_not_e[label] = n_not_e

        return label_freq_not_e



    def _single_get_w_label_freq(self):
        """single thread version of counting up (word, label) frequency

        :return:
        """
        word_label_freq_dict = {}
        for label in self.label_list:
            labeled_vocab = self.labeled_document[label]
            for word in self.vocabulary_list:
                freq_w_e = labeled_vocab.count(word)
                if word not in word_label_freq_dict:
                    word_label_freq_dict[word] = {label: freq_w_e}
                else:
                    word_label_freq_dict[word][label] = freq_w_e

        return word_label_freq_dict


    def _subtask_get_w_label_freq(self, label_word_tuple):
        """multi task version of (word, label) frequency

        :param label_word_tuple:
        :return:
        """
        assert isinstance(label_word_tuple, tuple)
        assert len(label_word_tuple) == 2

        label = label_word_tuple[0]
        word = label_word_tuple[1]

        labeled_vocab = self.labeled_document[label]
        freq_w_e = labeled_vocab.count(word)

        return {"word": word, "label": label, "freq": freq_w_e}


    def _get_w_label_freq(self, n_thread):
        """get frequencies of (w, label)

        :param n_thread:
        :return:
        """

        if n_thread > 1:
            subtask_tuple_list = self._make_label_word_task_tuples()
            pool = multiprocessing.Pool(processes=n_thread)
            results = pool.map(unwrap_self_count_get_freq_w_e, zip([self]*len(subtask_tuple_list), subtask_tuple_list))
            word_label_freq_dict = {}
            for counted_obj in results:
                if counted_obj['word'] not in word_label_freq_dict:
                    word_label_freq_dict[counted_obj['word']] = {counted_obj['label']: counted_obj['freq']}
                else:
                    word_label_freq_dict[counted_obj['word']][counted_obj['label']] = counted_obj['freq']

        else:
            word_label_freq_dict = self._single_get_w_label_freq()


        return word_label_freq_dict



    def _get_w_not_label_freq(self):
        """count up (w, not_label)

        :return:
        """
        w_not_e = {}
        for label in self.label_list:
            for word in self.vocabulary_list:
                freq_w_not_e = self.total_word_freq[word] - self.w_e_freq[word][label]

                if word not in w_not_e:
                    w_not_e[word] = {label: freq_w_not_e}
                else:
                    w_not_e[word][label] = freq_w_not_e

        return w_not_e


    def _soa_formula(self, freq_e, freq_not_e, freq_w_e, freq_w_not_e):
        nominator = (float(freq_w_e) * freq_not_e)
        denominator = (float(freq_e) * freq_w_not_e)
        if nominator==0 or denominator==0:
            return 0
        else:
            ans = nominator / denominator
            assert isinstance(ans, float)
            soa_val =  math.log(ans, 2)
            return soa_val


    def _soa_single_thread(self, is_zero):
        soa_scores = {}
        for label in self.label_list:
            freq_e = self.label_freq_dict[label]
            freq_not_e = self.label_freq_not_dict[label]
            for word in self.vocabulary_list:
                freq_w_e = self.w_e_freq[word][label]
                freq_w_not_e = self.w_not_e_freq[word][label]

                soa_val = self._soa_formula(freq_e=freq_e, freq_not_e=freq_not_e,
                                             freq_w_e=freq_w_e, freq_w_not_e=freq_w_not_e)

                if is_zero==False and soa_val == 0: continue

                if label not in soa_scores:
                    soa_scores[label] = [{"word": word, "score": soa_val}]
                else:
                    soa_scores[label].append({"word": word, "score": soa_val})

        return soa_scores



    def _subtask_func(self, arg_tuple):
        assert isinstance(arg_tuple, tuple)
        assert len(arg_tuple)==2
        label = arg_tuple[0]
        word = arg_tuple[1]

        freq_e = self.label_freq_dict[label]
        freq_not_e = self.label_freq_not_dict[label]
        freq_w_e = self.w_e_freq[word][label]
        freq_w_not_e = self.w_not_e_freq[word][label]
        soa_val = self._soa_formula(freq_e=freq_e, freq_not_e=freq_not_e,
                                    freq_w_e=freq_w_e, freq_w_not_e=freq_w_not_e)

        return_obj = {"word": word, "label": label, "score": soa_val}

        return return_obj


    def _make_label_word_task_tuples(self):
        """making tuples for parallel process

        :return:
        """
        task_tuples = []
        for label in self.label_list:
            for word in self.vocabulary_list:
                task_tuples.append( tuple([label, word]) )

        list_func_args = [
            (task_tuples[0], task_tuples[1])
            for subtask_number, task_tuples
            in enumerate(task_tuples)]

        return list_func_args


    def _soa_multi_process(self, n_thread, is_zero):
        task_tuples_list = self._make_label_word_task_tuples()

        pool = multiprocessing.Pool(processes=n_thread)
        results = pool.map(unwrap_self_f, zip([self]*len(task_tuples_list), task_tuples_list))

        assert len(results) == len(task_tuples_list)

        soa_scores = {}
        for soa_score_result in sorted(results, key=lambda x: x["score"], reverse=True):
            word = soa_score_result['word']
            label = soa_score_result['label']
            score = soa_score_result['score']

            if is_zero==False and score==0: continue

            if label not in soa_scores: soa_scores[label] = [{"word": word, "score": score}]
            else: soa_scores[label].append({"word": word, "score": score})
        logging.debug(msg="Finished Post process")

        return soa_scores


    def calc_soa(self, is_zero=False):
        """main method of SoA calculation

        :return:
        """
        # SoA = log_2{ (freq(w,e) * freq(not_e)) / (freq(e) * freq(w, not_e) )
        assert isinstance(is_zero, bool)

        if self.n_thread==1:
            soa_scores = self._soa_single_thread(is_zero)
        else:
            soa_scores = self._soa_multi_process(self.n_thread, is_zero)
        logging.debug(msg="Finished calculating score")

        return soa_scores





