from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from permissions import permissioned_login_required
import logging
from logic.menteelgc import MenteeLogic

mentee_blueprint = Blueprint('mentee', __name__)

handler = MenteeLogic()


@mentee_blueprint.route("/mentee")
#@permissioned_login_required(role="MENTEE", redirect_on_fail="/dashboard")
def mentee():
    return handler.mentee()

@mentee_blueprint.route("/mentee/preferences", methods=['POST', 'GET'])
def mentee_preferences():
    return handler.mentee_preferences(request)

@mentee_blueprint.route('/mentee/mentor-list')
def mentee_mentor_list():
    return handler.mentee_mentor_list(request)

@mentee_blueprint.route('/mentee/mentor/<k_number_mentor>')
def mentee_mentor(k_number_mentor):
    return handler.mentor_view(k_number_mentor)

