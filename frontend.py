from dash import dcc, html, Dash, dependencies

class Frontend:
    def __init__(self):
        self.input_fact = None
        self.app = Dash(__name__)

    def display_question(self, question_answers_pair):
        """Displays a question and answer options"""

        # Extract the answers from the question_answers_pair dictionary
        answers = [answer for answer in question_answers_pair['answers'].values()]

        self.app.layout = html.Div([
            html.H1('Select an answer'),
            dcc.Dropdown(
                id='answer-dropdown',
                options=[{'label': answer['text'], 'value': answer['fact']} for answer in answers],
                value=None
            ),
            html.Button('Submit', id='submit-button', n_clicks=0),

            # Hidden div used in callbacks
            html.Div(id='hidden-div', style={'display':'none'})
        ])

        @self.app.callback(
            dependencies.Output('hidden-div', 'children'),
            [
                dependencies.Input('submit-button', 'n_clicks'),
                dependencies.State('answer-dropdown', 'value')
            ],
        )
        def set_response(n_clicks, selected_answer):
            """Gets the selected answer and stores it in the input_fact variable"""

            if selected_answer:
                self.input_fact = question_answers_pair['answers'][selected_answer]['fact']
            else:
                self.input_fact = None

            return ''

        self.app.run_server(debug=True)

    def display_answer(self, answer):
        """Displays an answer"""

        self.app.layout = html.Div([
            html.H1('Answer'),
            html.P(answer)
        ])

        self.app.run_server(debug=True)

    def get_input(self):
        """
        Returns the input if it exists
        Returns None otherwise
        """

        if self.input_fact:
            input = self.input_fact
            self.input_fact = None
            return input