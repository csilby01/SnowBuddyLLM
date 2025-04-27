# SnowBuddyLLM
SnowBuddy is a chatbot that's purpose is to help the user understand the difference between products, the database where info is collected from is EVO. The model currently only can talk about snowboards and snowboard bindings

---

## How to run

Installing dependencies:
```
pip install -r requirements.txt
```
*WILL WAIT TO COMPLETE TO FINISH THIS SECTION*
---

## CURRENT STATE:
- Model works for one or two product comparisons.
- Model cannot recall previous conversations due to context window limitations
- Model's RAG component does not always correctly select items, especially when one item includes the full name of another.

---

## To-do:
- Add review opinions (need larger context window)
- Improve model behavior
- Consider PEFT model

---