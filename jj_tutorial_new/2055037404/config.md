If you want to use different field names, edit the following variables:
(**You need to restart Anki for the changes take effect**).

* **"expressionField"**: (default: "Japanese") This is the field that has the Japanese word that will be searched in weblio.

* **"definitionField"**: (default: "JapaneseExpression") This field will receive the fetched definition from weblio.

Other variables: 
(No need to restart)

* **"max_threads"**: (default: 15) The number of words that will be fetched simultaneously from weblio.
  A very high number (50) can trigger weblio's DDoS protection and result in no results.

* **"force_update"**: (default: "no") If this variable value is `"no"`, skip the cards which `jap_defField` is not empty.
  If it is `"overwrite"`, the current contents are overwritten by the fetched definition.
  If it is `"append"`, the fetched definition is inserted after the current contents.

* **"update_separator"**: (default: `"<br>"`) When `force_update` is set to append, this string is used to separate the current contents and the fetched definition.
  `<br>` inserts a newline.
