
import csv
import logging
import os

import numpy as np
import pandas as pd


def backup(session: list) -> bool:
	"""Method to backup details for the current session.

	Args:
		session (list): Session metadata container.

	Returns:
		bool: Status flag indicatig successful backup of session metadata.
	"""
	# Process session information
	username = "_".join([x.upper() for x in session["username"].split()])
	subject_name = session["subject_name"].strip().upper()
	subject_id = session["subject_id"].strip()
	test_type = ["Objective" if session["test_id"] == "0" else "Subjective"][0]
	test_id = session["test_id"]
	timestamp = session["date"]
	status = False

	# Construct login data
	row = [
		timestamp,
		username,
		subject_name,
		subject_id,
		test_type,
		test_id,
		session["score"],
		session["result"]
	]

	# Push session metadata to a central repo
	filepath = session["database_path"]
	if os.path.isfile(filepath):
		try:
			with open(filepath, mode="a") as fp:
				fp_writer = csv.writer(fp)
				fp_writer.writerow(row)
				status = True
		except Exception as e:
			logging.exception("Exception raised at `backup`.", exc_info=True)
	else:
		print("Database placeholder nott found!")
	return status


def relative_ranking(session: list) -> tuple:
	"""Method to compute relative ranking for a particular user response.

	Args:
		session (list): Session metadata container.

	Returns:
		tuple: Tuple with max, min and mean score.
	"""
	min_scope, max_score = 0.0, 100.0
	mean_score = None

	def rounder(value, decimals=2):
		return np.round(value, decimals=decimals)

	# Load session meta to central repository
	try:
		df = pd.read_csv(session["database_path"])
	except Exception as e:
		logging.exception("Exception raised at `relative_ranking`.", exc_info=True)
	else:
		# Create relative score
		df = df[(df["SUBJECT_ID"] == int(session["subject_id"])) & (df["TEST_ID"] == int(session["test_id"]))]
		if df.shape[0] >= 1:
			max_score = rounder(df["SCORE"].max(), decimals=2)
			min_score = rounder(df["SCORE"].min(), decimals=2)
			mean_score = rounder(df["SCORE"].mean(), decimals=2)
	finally:
		return (max_score, min_score, mean_score)
