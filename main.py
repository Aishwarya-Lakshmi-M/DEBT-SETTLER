import streamlit as st
from collections import defaultdict

# Function to calculate minimum transactions
def minTransfers(transactions):
    score = defaultdict(int)
    for f, t, a in transactions:
        score[f] -= a
        score[t] += a
    
    positives = [(k, v) for k, v in score.items() if v > 0]
    negatives = [(k, v) for k, v in score.items() if v < 0]

    def recurse(positives, negatives):
        if not positives and not negatives:
            return 0, []

        min_count = float('inf')
        min_transactions = []

        negative = negatives[0]

        for positive in positives:
            new_positives = positives.copy()
            new_negatives = negatives.copy()
            new_positives.remove(positive)
            new_negatives.remove(negative)

            transactions = []
            if positive[1] == -negative[1]:
                transaction_count, sub_transactions = recurse(new_positives, new_negatives)
                transactions = [(negative[0], positive[0], positive[1])] + sub_transactions
            elif positive[1] > -negative[1]:
                new_positives.append((positive[0], positive[1] + negative[1]))
                transaction_count, sub_transactions = recurse(new_positives, new_negatives)
                transactions = [(negative[0], positive[0], -negative[1])] + sub_transactions
            else:
                new_negatives.append((negative[0], positive[1] + negative[1]))
                transaction_count, sub_transactions = recurse(new_positives, new_negatives)
                transactions = [(negative[0], positive[0], positive[1])] + sub_transactions

            if transaction_count + 1 < min_count:
                min_count = transaction_count + 1
                min_transactions = transactions

        return min_count, min_transactions

    return recurse(positives, negatives)

# Streamlit UI
st.title('Debt Settlement Calculator')

# Input the number of transactions
num_transactions = st.number_input('Enter the number of transactions:', min_value=1, step=1)

# Input the transactions
transactions = []
for i in range(num_transactions):
    st.write(f'Transaction {i+1}')
    from_person = st.text_input(f'From (person {i+1}):', key=f'from_{i}')
    to_person = st.text_input(f'To (person {i+1}):', key=f'to_{i}')
    amount = st.number_input(f'Amount (transaction {i+1}):', min_value=1, step=1, key=f'amount_{i}')
    transactions.append([from_person, to_person, amount])

# Calculate minimum transactions
if st.button('Calculate'):
    count, transactions_needed = minTransfers(transactions)
    st.write(f'Minimum number of transactions needed: {count}')
    st.write('Transactions to settle the debt:')
    for t in transactions_needed:
        st.write(f'{t[0]} pays {t[1]} an amount of {t[2]}')

# Run the app
if __name__ == '__main__':
    st.run()
