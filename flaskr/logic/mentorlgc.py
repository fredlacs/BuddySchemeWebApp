import logging

from flask import flash, redirect, render_template, url_for, abort
from flask_login import current_user

from flaskr.forms import MentorPreferencesForm
from flaskr.models.allocationmdl import AllocationModel
from flaskr.models.hobbymdl import HobbyModel
from flaskr.models.interestmdl import InterestModel
from flaskr.models.student_hobbymdl import StudentHobbyModel
from flaskr.models.student_interestmdl import StudentInterestModel
from flaskr.models.studentmdl import StudentModel


class MentorLogic:

    def mentor(self):

        try:
            data_definitions = self.get_data_definitions()
            user_data = self.get_all_user_data(current_user.scheme_id, current_user.k_number)

            return render_template("user_screens/mentor/mentor_dashboard_page.html", title="Your Profile", user_data=user_data)

        except Exception:
            self._log.exception("Could not execute get mentor logic")
            return abort(500)

    def mentor_preferences(self, request):
        try:
            user_data = self.get_all_user_data(current_user.scheme_id, current_user.k_number)

            # Create new form and pre-populate with existing values
            form = MentorPreferencesForm(request.form, date_of_birth=user_data["date_of_birth"], gender=user_data["gender"],
                                         buddy_limit=user_data["buddy_limit"], interests=user_data["interests"], hobbies=user_data["hobbies"])

            # Update data on form submission
            if request.method == "POST":
                self._update_mentee(request.form.getlist('hobby'), request.form.getlist('interest'),
                                    request.form['date_of_birth'], request.form['gender'])

                return redirect(url_for("mentor.mentor"))
            else:
                # Pre-populate interest and hobbies with existing values
                form.interests.data = [interest_id for interest_id,
                                       interest_name in user_data["interests"].items()]
                form.hobbies.data = [hobby_id for hobby_id,
                                     hobby_name in user_data["hobbies"].items()]

                # Populate possible choices using data from data_definitions
                data_definitions = self.get_data_definitions()
                gender_definitions = self.get_gender_definitions()

                form.gender.choices = [(gender_type, gender_type)
                                       for gender_type in gender_definitions]
                form.interests.choices = [(interest["id"], interest["interest_name"])
                                          for interest in data_definitions["interests"]]
                form.hobbies.choices = [(hobby["id"], hobby["hobby_name"])
                                        for hobby in data_definitions["hobbies"]]

                return render_template("user_screens/mentor/mentor_preferences_page.html", title="Your Preferences", user_data=user_data, form=form)

        except Exception:
            self._log.exception("Could not execute mentor preferences logic")
            return abort(500)

    def _update_mentor(self, hobbies, interests, date_of_birth, gender):
        self._student_hobby_handler.update_hobbies(
            current_user.scheme_id, current_user.k_number, hobbies)
        self._student_interest_handler.update_interests(
            current_user.scheme_id, current_user.k_number, interests)
        self._student_handler.update_date_of_birth(
            current_user.scheme_id, current_user.k_number, date_of_birth)
        self._student_handler.update_gender(
            current_user.scheme_id, current_user.k_number, gender)

    def mentor_delete(self, request):
        """ Will delete all the mentors informations from the database"""

        try:
            if request.method == "POST":
                flash("Be careful you are about to delete all of your data")
                self._student_handler.delete_students(current_user.scheme_id, current_user.k_number)
                return redirect(url_for("mentor.mentor"))
            else:
                return render_template("user_screens/mentor/mentor_delete_page.html")

        except Exception:
            self._log.exception("Could not delete student")
            return abort(500)

    def mentor_mentee_list(self, request):

        try:
            mentee_list = self._allocation_handler.get_mentees(
                current_user.scheme_id, current_user.k_number)

            # Object to hold all the mentees. This takes the form of a nested dictionary indexed by k_numbers
            mentee_list_data = {}

            # Format results into nested dict for use on page
            for mentee in mentee_list:
                mentee_k_number = mentee['mentee_k_number']
                mentee_list_data[mentee_k_number] = self._student_handler.get_user_data(
                    current_user.scheme_id, mentee_k_number)

            return render_template("user_screens/mentor/mentor_mentee_list_page.html", title="Your Mentees", mentees=mentee_list_data)

        except Exception:
            self._log.exception("Could not execute mentor mentee list logic")
            return abort(500)

    def mentee_view(self, k_number_mentee):

        try:
            return render_template("user_screens/mentor/mentor_mentee_page.html", title="Your Mentee", mentee_data=self._student_handler.get_user_data(current_user.scheme_id, k_number_mentee), k_number_mentee=k_number_mentee)

        except Exception:
            self._log.exception("Could not execute mentee view logic")
            return abort(500)

    # HELPER FUNCTIONS

    def get_gender_definitions(self):
        """Get a list of all possible gender types"""
        try:
            return ["Male", "Female", "Other", "Prefer not to say"]

        except Exception:
            self._log.exception("Could not execute mentor get gender definitions logic")
            return abort(500)

    def get_data_definitions(self):
        """ Get a list of all possible hobbies and interests """
        try:
            data_definitions = {
                "hobbies": self._hobby_handler.get_hobby_list(),
                "interests": self._interest_handler.get_interest_list()
            }

            return data_definitions

        except Exception:
            self._log.exception("Could not execute mentor get data definitions logic")
            return abort(500)

    def get_all_user_data(self, scheme_id, k_number):
        """ Get all user data from database and format into a single dict"""
        try:
            user_data = self._student_handler.get_user_data(scheme_id, k_number)

            # retrieve interests from db and format into a list
            interests = {}
            for interest in self._student_interest_handler.get_interests(scheme_id, k_number):
                interests[interest["interest_id"]] = interest["interest_name"]

            user_data["interests"] = interests

            # retrieve hobbies from db and format into a list
            hobbies = {}
            for hobby in self._student_hobby_handler.get_hobbies(scheme_id, k_number):
                hobbies[hobby["hobby_id"]] = hobby["hobby_name"]

            user_data["hobbies"] = hobbies

            return user_data

        except Exception:
            self._log.exception("Could not execute get all user data logic")
            return abort(500)

    def __init__(self):
        try:
            self._log = logging.getLogger(__name__)
            self._allocation_handler = AllocationModel()
            self._student_handler = StudentModel()
            self._student_hobby_handler = StudentHobbyModel()
            self._student_interest_handler = StudentInterestModel()
            self._hobby_handler = HobbyModel()
            self._interest_handler = InterestModel()
        except Exception:
            self._log.exception("Could not create model instance")
            raise abort(500)
