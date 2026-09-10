Here is the current **LongStoryGoes development log** from our work so far:

* **Repository:** [CyrilPec/LongStoryGoes](https://github.com/CyrilPec/LongStoryGoes?utm_source=chatgpt.com)
* **Branch:** `main`
* **Current architecture:** `000.py` → fundamental world; `001.py` → time/continuity; `002.py` → development philosophy/log.
* **Core principle:** the world is the main character and grows one connected file at a time. No complete world is designed in advance.
* **Story structure:** each file is a node in a growing world graph. Locations, objects, characters, relationships, events, rules and consequences persist when relevant.
* **World time:** the world has its own time and history. Characters and objects exist in time; events have consequences; the world continues when nobody observes it.
* **AI:** an agent inside the world. It observes the current node, understands state/relationships, chooses actions, executes them, observes consequences, and continues.
* **Languages:** the project evolved from “English + Python” into a **single hybrid story language**.
* **Important refinement:** Python is not merely a technical translation of English. Python becomes part of the grammar of the story.
* **Mapping being developed:**

  * nouns → objects / variables
  * verbs → methods / functions / actions
  * adjectives → properties / states
  * adverbs → parameters / modifiers
  * relationships → attributes / references
  * time → state/history
  * consequences → executable state changes
* **Writing principle:** English and Python should be **mixed**, rather than having a separate English narrative and separate Python description.
* **Current experimental form:** an English sentence can introduce or extend a Python expression, and Python can represent the actual grammatical operation:
  `glass.state = "broken"` → adjective/state
  `boy.look_at(glass)` → verb/action
  `boy = Character(...)` → noun/entity
* **Important narrative rule:** Python should establish the concrete world operation; the English around it should add meaning, consequence, observation, or the next idea—not simply repeat what the code already says.
* **Formatting preference:** compact, no unnecessary empty lines.
* **Current direction:** develop the hybrid language organically through the story itself rather than designing a complete grammar beforehand.
* **Next conceptual step:** make a short story where **English and Python are genuinely mixed inside the same flow**, so Python functions as English verbs/adjectives/etc., rather than using Python followed by ordinary comments.
