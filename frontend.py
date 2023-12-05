from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    answer = RadioField('Answer', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')


class Frontend:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'ktp'
        self.setup_routes()

        self.controller = None

        self.question_answers_pair = None
        self.selected_answer = None

    def set_controller(self, controller):
        self.controller = controller

    def setup_routes(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def view():

            # Skip if no question is set
            if not (self.question_answers_pair or self.selected_answer):
                return render_template('404.html')

            if self.question_answers_pair:

                form = QuestionForm()
                form.answer.choices = [(answer['fact'], answer['text']) for answer in self.question_answers_pair['answers'].values()]

                if form.validate_on_submit():
                    self.selected_answer = form.answer.data
                    self.controller.update_model(self.selected_answer)
                    return redirect('/')

                return render_template('question.html', form=form, question=self.question_answers_pair['text'])

            return render_template('answer.html', answer=self.selected_answer)

        @self.app.route('/reset')
        def reset():
            self.selected_answer = None
            self.question_answers_pair = None
            self.controller.reset()
            return redirect('/')

    def get_input(self):
        return self.selected_answer

    def set_question(self, question):
        self.question_answers_pair = question
        self.selected_answer = None

    def display_answer(self, answer):
        self.selected_answer = answer
        self.question_answers_pair = None

        print(answer)

    def run(self):
        self.app.run(debug=True)


if __name__ == '__main__':
    frontend = Frontend()
    frontend.run()
