from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired
import os


class QuestionForm(FlaskForm):
    answer = RadioField('Answer', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')


class Frontend:
    """
    This class is responsible for the frontend of the application.
    It is a Flask application that is running in a separate thread.
    """

    def __init__(self):
        """
        Creates a frontend for the application
        Sets up the routes for the application and create variables for the question and answer
        """
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'ktp'
        self.setup_routes()

        self.controller = None

        self.question_answers_pair = None
        self.selected_answer = None

        self.images = os.listdir('static')

    def set_controller(self, controller):
        """
        Sets the controller for the frontend
        Allows the frontend to communicate with the model
        """
        self.controller = controller

    def setup_routes(self):
        """
        Sets up the webpages to be displayed
        When the user visits the root page, the question page is displayed
        Once all questions are answered, the answer page is displayed
        """
        @self.app.route('/', methods=['GET', 'POST'])
        def view():

            # Skip if no question is set
            if not (self.question_answers_pair or self.selected_answer):
                return render_template('404.html')

            if self.question_answers_pair:

                form = QuestionForm()
                form.answer.choices = [(answer['fact'], answer['text']) for answer in self.question_answers_pair['answers'].values()]

                print(form.answer.choices)

                if form.validate_on_submit():
                    self.selected_answer = form.answer.data
                    self.controller.update_model(self.selected_answer)
                    return redirect('/')

                return render_template('question.html', form=form, question=self.question_answers_pair['text'], filenames=self.images)

            return render_template('answer.html', answer=self.selected_answer)

        @self.app.route('/reset')
        def reset():
            self.selected_answer = None
            self.question_answers_pair = None
            self.controller.reset()
            return redirect('/')

        @self.app.template_filter('is_list')
        def is_list(value):
            """
            Returns True if the value is a list
            """
            return isinstance(value, list)

    def get_input(self):
        """
        Returns the answer selected by the user
        """
        return self.selected_answer

    def set_question(self, question):
        """
        Allows the controller to set the question to be displayed
        """
        self.question_answers_pair = question
        self.selected_answer = None

    def display_answer(self, answer):
        """
        Allows the controller to display the answer to the user
        """
        self.selected_answer = answer
        self.question_answers_pair = None

        print(answer)

    def run(self):
        """
        Runs the frontend application
        """
        self.app.run(debug=True)


if __name__ == '__main__':
    frontend = Frontend()
    frontend.run()
