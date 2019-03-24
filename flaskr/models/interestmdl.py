from flaskr.models.helpers import sanity_check, to_str
from flaskr.models.basicmdl import BasicModel
import logging

class InterestModel(BasicModel):

    def delete_interest(self, interest_id, scheme_id=1): # remove default
        """ Given the interest_id will delete the interest"""

        try:
            self._dao.execute("DELETE FROM Interest WHERE id = % AND scheme_id = %s;", (interest_id, scheme_id))
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not delete the interest")
            raise e


    def insert_interest(self, interest, scheme_id=1):
        """ Will insert an entry for a interest into the database"""
        try:
            self._dao.execute("INSERT INTO Interest (interest_name) VALUES(%s, %s);", (scheme_id, interest))
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not insert the interest")
            raise e

    def get_interest_list(self, scheme_id=1):
        """ Will retrieve a list of possible hobbies from the database"""

        try:
            return self._dao.execute("SELECT * FROM Interest WHERE scheme_id = %s;", (scheme_id, ))

        except Exception as e:
            self._log.exception("Could not get the list of hobbies")
            raise e
