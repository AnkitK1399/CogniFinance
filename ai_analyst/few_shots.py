few_shots = [
                {
                    "Question":"How many users had income transactions greater than 2,000 between march 02, 2026, and march 22, 2026?",
                    "SQLquery":"SELECT COUNT(DISTINCT user_id) AS user_count FROM transaction WHERE transaction_type = 'INCOME' AND amount > 2000 AND date BETWEEN '2026-03-02' AND '2026-03-22';",
                    "Results":"Result of the SQL query",
                    "Answers":"3"
                },

                {
                    "Question":"How many users are there whose ai summary has  been created?",
                    "SQLquery":"SELECT COUNT(user_id) FROM ai_analyst_aisummary;",
                    "Results":"Result of the SQL query",
                    "Answers":"1"
                },

                {
                    "Question":"How many users are have positive balance?",
                    "SQLquery":"SELECT COUNT(DISTINCT id) from users_user WHERE current_balance > 0;",
                    "Results":"Result of the SQL query",
                    "Answers":"7"
                },

                {
                    "Question":"What is the spending by a user in month march?",
                    "SQLquery":"SELECT SUM(amount) from transactions_transaction WHERE user_id = 6 AND  transaction_type = 'EXPENSE' AND date BETWEEN '2026-03-02' AND '2026-03-22';",
                    "Results":"Result of the SQL query",
                    "Answers":"4037"
                }

    
]