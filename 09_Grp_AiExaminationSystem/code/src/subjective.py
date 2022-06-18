import logging
from typing import Tuple

import nltk as nlp
import numpy as np


class SubjectiveTest:
	"""Class abstraction for subjective test generation module.
	"""

	def __init__(self, filepath: str):
		"""Class constructor.

		Args:
			filepath (str): Absolute filepath to the subject corpus.
		"""
		self.question_pattern = [
			"Explain in detail ",
			"Define ",
			"Write a short note on ",
			"What do you mean by "
		]

		self.grammar = r"""
			CHUNK: {<NN>+<IN|DT>*<NN>+}
			{<NN>+<IN|DT>*<NNP>+}
			{<NNP>+<NNS>*}
		"""

		try:
			with open(filepath, mode="r") as fp:
				self.summary = fp.read()
		except FileNotFoundError:
			logging.exception("Corpus file not found.", exc_info=True)

	@staticmethod
	def word_tokenizer(sequence: str) -> list:
		"""Tokenize string sequences to words.

		Args:
			sequence (str): Corpus sequences.

		Returns:
			list: Word tokens.
		"""
		word_tokens = list()
		try:
			for sent in nlp.sent_tokenize(sequence):
				for w in nlp.word_tokenize(sent):
					word_tokens.append(w)
		except Exception:
			logging.exception("Word tokenization failed.", exc_info=True)
		return word_tokens

	@staticmethod
	def create_vector(answer_tokens: list, tokens: list) -> np.array:
		"""Create a one-hot encoded vector for the answer_tokens.

		Args:
			answer_tokens (list): Tokenized user response.
			tokens (list): Tokenized answer corpus.

		Returns:
			np.array: A one-hot encoded vector of the answer.
		"""
		return np.array([1 if tok in answer_tokens else 0 for tok in tokens])

	@staticmethod
	def cosine_similarity_score(vector1: np.array, vector2: np.array) -> float:
		"""Compute the euclidean distance between two vectors.

		Args:
			vector1 (np.array): Actual answer vector.
			vector2 (np.array): User response vector.

		Returns:
			float: Euclidean distance between two vectors.
		"""
		def vector_value(vector):
			return np.sqrt(np.sum(np.square(vector)))

		v1 = vector_value(vector1)
		v2 = vector_value(vector2)

		v1_v2 = np.dot(vector1, vector2)
		return (v1_v2 / (v1 * v2)) * 100

	def generate_test(self, num_questions: int = 2) -> Tuple[list, list]:
		"""Method to generate subjective test.

		Args:
			num_questions (int, optional): Maximum number of questions
				to be generated. Defaults to 2.

		Returns:
			Tuple[list, list]: Generated `Questions` and `Answers` respectively
		"""
		try:
			sentences = nlp.sent_tokenize(self.summary)
		except Exception:
			logging.exception("Sentence tokenization failed.", exc_info=True)

		try:
			cp = nlp.RegexpParser(self.grammar)
		except Exception:
			logging.exception("Regex grammar train failed.", exc_info=True)

		question_answer_dict = dict()
		for sentence in sentences:

			try:
				tagged_words = nlp.pos_tag(nlp.word_tokenize(sentence))
			except Exception:
				logging.exception("Word tokenization failed.", exc_info=True)

			tree = cp.parse(tagged_words)
			for subtree in tree.subtrees():
				if subtree.label() == "CHUNK":
					temp = ""
					for sub in subtree:
						temp += sub[0]
						temp += " "
					temp = temp.strip()
					temp = temp.upper()
					if temp not in question_answer_dict:
						if len(nlp.word_tokenize(sentence)) > 20:
							question_answer_dict[temp] = sentence
					else:
						question_answer_dict[temp] += sentence

		keyword_list = list(question_answer_dict.keys())
		question_answer = list()

		for _ in range(3):
			rand_num = np.random.randint(0, len(keyword_list))
			selected_key = keyword_list[rand_num]
			answer = question_answer_dict[selected_key]
			rand_num %= 4
			question = self.question_pattern[rand_num] + selected_key + "."
			question_answer.append({"Question": question, "Answer": answer})

		que = list()
		ans = list()
		while len(que) < num_questions:
			rand_num = np.random.randint(0, len(question_answer))
			if question_answer[rand_num]["Question"] not in que:
				que.append(question_answer[rand_num]["Question"])
				ans.append(question_answer[rand_num]["Answer"])
			else:
				continue
		return que, ans

	def evaluate_subjective_answer(self, original_answer: str, user_answer: str) -> float:
		"""Evaluate the subjective answer given by the user.

		Args:
			original_answer (str): A string representing the original answer.
			user_answer (str): A string representing the answer given by the user.

		Returns:
			float: Similarity/correctness score of the user answer
				based on the original answer.
		"""
		score_obt = 0
		original_ans_list = self.word_tokenizer(original_answer)
		user_ans_list = self.word_tokenizer(user_answer)

		overall_list = original_ans_list + user_ans_list

		vector1 = self.create_vector(original_ans_list, overall_list)
		vector2 = self.create_vector(user_answer, overall_list)

		score_obt = self.cosine_similarity_score(vector1, vector2)
		return score_obt
