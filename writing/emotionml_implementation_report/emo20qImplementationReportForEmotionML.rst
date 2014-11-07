================================================================
EmotionML Implementation Report: Web-based EMO20Q Dialog Agent
================================================================

:authors: Abe Kazemzadeh and Shrikanth Narayanan
:organization: University of Southern California Signal Analysis and Interpretation Laboratory (SAIL)

Summary
=================

Emotion twenty questions (EMO20Q) is a experimental framework for studying how
people describe emotions in language and how computers can simulate this type
of verbal behavior.  In EMO20Q, the familiar spoken parlor game of twenty
questions is restricted to words that players feel refers to emotions.  

In this implementation report, we examine the case where a server-side
computer agent plays the role of the questioner and a human plays the answerer
via a web browser.  

The EMO20Q questioner agent can be decomposed into several components, notably
a **vocabulary**, **semantic knowledge**, an **episodic buffer**, and a
**belief state**.  The vocabulary is a list of 110 emotion words and this
vocabulary is expected to grow over time as more data is collected, but
remains constant during the agent's instantiation.  Semantic knowledge is a
large object that remains the same across different agent instantiations and
states, while the episodic buffer and belief state are smaller objects that
vary over time for each interactive session. Because of the size of the
semantic knowledge object, serialization of the agent for each session is not
possible.  Rather, the episodic buffer and belief states are serialized while
the semantic knowledge persists as a static object in the server memory. The
belief state is represented as a probability vector indexed by items of the
vocabulary.

EmotionML is used to implement the questioner agent's vocabulary and belief
state. The agent's vocabulary is implemented using the EmotionML
``vocabulary`` idiom and the agent's belief state is represented using the
``emotion`` idiom with a ``category`` as a child and the ``value`` attribute
to hold numerical probability values.

EmotionML Test Assertions
============================

:note: NI stands for Not Implemented

Document Structure
-------------------
100 : All EmotionML documents must validate against the XML schema.
  pass (provided single word emotion names)
101 : The root element of standalone EmotionML documents MUST be <emotionml>  
  pass
102 : The <emotionml> element MUST define the EmotionML namespace: "http://www.w3.org/2009/10/emotionml".
  pass
103 : The <emotionml> element MAY contain one or more <emotion> elements.
  pass
104 : The <emotionml> element MAY contain one or more <vocabulary> elements.
  pass
105 : The <emotionml> element MAY contain a single <info> element.
  NI
110 : The root element of a standalone EmotionML document MUST have an attribute "version".
  pass
111 : The "version" attribute of <emotionml> MUST have the value "1.0"
  pass
112 : The <emotionml> element MAY contain an attribute "category-set".
  pass
113 : The "category-set" attribute of <emotionml>, if present, MUST be of type xsd:anyURI.
  pass
114 : SUB CONSTRAINT: The "category-set" attribute of <emotionml>, if present, MUST refer to the ID of a <vocabulary> element with type="category".
  pass
115 : The <emotionml> element MAY contain an attribute "dimension-set".
  NI
116 : The "dimension-set" attribute of <emotionml>, if present, MUST be of type xsd:anyURI.
  NI
117 : SUB CONSTRAINT: The "dimension-set" attribute of <emotionml>, if present, MUST refer to the ID of a <vocabulary> element with type="dimension".
  NI
118 : The <emotionml> element MAY contain an attribute "appraisal-set".
  NI
119 : The "appraisal-set" attribute of <emotionml>, if present, MUST be of type xsd:anyURI.
  NI
120 : SUB CONSTRAINT: The "appraisal-set" attribute of <emotionml>, if present, MUST refer to the ID of a <vocabulary> element with type="appraisal".
  NI
121 : The <emotionml> element MAY contain an attribute "action-tendency-set".
  NI
122 : The "action-tendency-set" attribute of <emotionml>, if present, MUST be of type xsd:anyURI.
  NI
123 : SUB CONSTRAINT: The "action-tendency-set" attribute of <emotionml>, if present, MUST refer to the ID of a <vocabulary> element with type="action-tendency".
  NI
124 : The <emotionml> element MAY contain arbitrary plain text.
  NI
150 : The <emotion> element MAY contain one or more <category> elements.
  pass
151 : The <emotion> element MAY contain one or more <dimension> elements.
  NI
152 : The <emotion> element MAY contain one or more <appraisal> elements.
  NI
153 : The <emotion> element MAY contain one or more <action-tendency> elements.
  NI
154 : The <emotion> element MAY contain one or more <reference> elements.
  NI
155 : The <emotion> element MAY contain a single <info> element.
  NI
156 : The <emotion> element MUST contain at least one <category> or <dimension> or <appraisal> or <action-tendency> element.
  pass
157 : The allowed child elements of <emotion> MAY occur in any order.
  pass
158 : The allowed child elements of <emotion> MAY occur in any combination.
  pass
159 : The <emotion> element MAY contain an attribute "category-set".
  NI
160 : The "category-set" attribute of <emotion>, if present, MUST be of type xsd:anyURI.
  pass
161 : SUB CONSTRAINT: The "category-set" attribute of <emotion>, if present, MUST refer to the ID of a <vocabulary> element with type="category".
  pass
162 : The <emotion> element MAY contain an attribute "dimension-set".
  NI	
163 : The "dimension-set" attribute of <emotion>, if present, MUST be of type xsd:anyURI.
  NI
164 : SUB CONSTRAINT: The "dimension-set" attribute of <emotion>, if present, MUST refer to the ID of a <vocabulary> element with type="dimension".
  NI
165 : The <emotion> element MAY contain an attribute "appraisal-set".
  NI
166 : The "appraisal-set" attribute of <emotion>, if present, MUST be of type xsd:anyURI.
  NI
167 : SUB CONSTRAINT: The "appraisal-set" attribute of <emotion>, if present, MUST refer to the ID of a <vocabulary> element with type="appraisal".
  NI
168 : The <emotion> element MAY contain an attribute "action-tendency-set".
  NI
169 : The "action-tendency-set" attribute of <emotion>, if present, MUST be of type xsd:anyURI.	
  NI
170 : SUB CONSTRAINT: The "action-tendency-set" attribute of <emotion>, if present, MUST refer to the ID of a <vocabulary> element with type="action-tendency".	
  NI
171 : The <emotion> element MAY have an attribute "version".
  pass
172 : The "version" attribute of <emotion>, if present, MUST have the value "1.0".
  pass			
173 : The <emotion> element MAY contain an attribute "id".
  NI
174 : The "id" attribute of <emotion>, if present, MUST be of type xsd:ID.
  NI
175 : The <emotion> element MAY have an attribute "start".
  NI
176 : The <emotion> element MAY have an attribute "end".
  NI
177 : The <emotion> element MAY have an attribute "duration".
  NI
178 : The <emotion> element MAY have an attribute "time-ref-uri".
  NI
179 : The <emotion> element MAY have an attribute "time-ref-anchor-point".
  NI
180 : The <emotion> element MAY have an attribute "offset-to-start".
  NI
181 : The <emotion> element MAY have an attribute "expressed-through".
  NI
182 : The <emotion> element MAY contain arbitrary plain text.
  NI

Representations of emotions and related states
-------------------------------------------------

210 : If the <category> element is used, a category vocabulary MUST be declared using a "category-set" attribute on either the enclosing <emotion> element or the root element <emotionml>.
  pass
211 :A category element MUST contain a "name" attribute.
  pass
212 : SUB CONSTRAINT: The value of the "name" attribute of the <category> element MUST be contained in the declared category vocabulary. If both the <emotionml> and the <emotion> element has a "category-set" attribute, then the <emotion> element's attribute defines the declared category vocabulary.
  pass
213 : For any given category name in the set, zero or one occurrence is allowed within an <emotion> element, i.e. a category with name "x" MUST NOT appear twice in one <emotion> element.
  pass
214 : A <category> MAY contain a "value" attribute.
  pass
215 : A <category> MAY contain a <trace> element.
  NI
216 : A <category> MUST NOT contain both a "value" attribute and a <trace> element.
  pass
217 : A <category> element MAY contain a "confidence" attribute.
  NI
220 : If the <dimension> element is used, a dimension vocabulary MUST be declared using a "dimension-set" attribute on either the enclosing <emotion> element or the root element <emotionml>.
  NI
221 : A <dimension> element MUST contain a "name" attribute.
  NI
222 : CONSTRAINT: The value of the "name" attribute of the <dimension> element MUST be contained in the declared dimension vocabulary. If both the <emotionml> and the <emotion> element has a "dimension-set" attribute, then the <emotion> element's attribute defines the declared dimension vocabulary.
  NI
223 : For any given dimension name in the set, zero or one occurrence is allowed within an <emotion> element i.e. a dimension with name "x" MUST NOT appear twice in one <emotion> element.
  NI
224 : A <dimension> MUST contain either a "value" attribute or a <trace> element.
  NI
225 : A <dimension> element MAY contain a "confidence" attribute.
  NI
230 : If the <appraisal> element is used, an appraisal vocabulary MUST be declared using an "appraisal-set" attribute on either the enclosing <emotion> element or the root element <emotionml>.
  NI
231 : An <appraisal> element MUST contain the "name" attribute.
  NI
232 : SUB CONSTRAINT: The value of the "name" attribute of the <appraisal> element MUST be contained in the declared appraisal vocabulary. If both the <emotionml> and the <emotion> element has an "appraisal-set" attribute, then the <emotion> element's attribute defines the declared appraisal vocabulary.
  NI
233 : For any given appraisal name in the set, zero or one occurrence is allowed within an <emotion> element, i.e. an appraisal with name "x" MUST NOT appear twice in one <emotion> element.
  NI
234 : An  <appraisal> element MAY contain a "value" attribute.
  NI
235 : An <appraisal> element MAY contain a <trace> element.
  NI
236 : An <apraisal> element MUST NOT contain both a "value" attribute and a <trace> element.
  NI
237 : An <appraisal> element MAY contain a "confidence" attribute. 
  NI
240 : If the <action-tendency> element is used, an action tendency vocabulary MUST be declared using an "action-tendency-set" attribute on either the enclosing <emotion> element or the root element <emotionml>.
  NI
241 : An <action-tendency> element MUST contain the "name" attribute.
  NI
242 : SUB CONSTRAINT: The value of the "name" attribute of the <action-tendency> element MUST be contained in the declared action tendency vocabulary. If both the <emotionml> and the <emotion> element has an "action-tendency-set" attribute, then the <emotion> element's attribute defines the declared action tendency vocabulary.
  NI
243 : For any given action tendency name in the set, zero or one occurrence is allowed within an <emotion> element, i.e. an action tendency with name "x" MUST NOT appear twice in one <emotion> element.
  NI
244 : An <action-tendency> element MAY contain a "value" attribute.
  NI
245 : An <action-tendency> element MAY contain a <trace> element.
  NI
246 : An <action-tendency> element MUST NOT contain both a "value" attribute and a <trace> element.
  NI
247 : An <action-tendency> element MAY contain a "confidence" attribute.
  NI

Meta-information
-------------------
300 : The value of the "confidence" attribute MUST be a floating point number in the closed interval [0, 1].
  NI
301 : The attribute "expressed-through" of the <emotion> element, if present, MUST be of type xsd:nmtokens.
  NI
302 : The <info> element MAY contain any elements with a namespace different from the EmotionML namespace, "http://www.w3.org/2009/10/emotionml".
  NI
303 : The <info> element MAY contain arbitrary plain text.
  NI
304 : The <info> element MUST NOT contain any elements in the EmotionML namespace, "http://www.w3.org/2009/10/emotionml".
  NI
305 : The <info> element MAY contain an attribute "id".
  NI
306 : The "id" attribute of the <info> element, if present, MUST be of type xsd:ID.
  NI

References and time
--------------------
410 : The <reference> element MUST contain a "uri" attribute.
  NI
411 : The "uri" attribute of <reference> MUST be of type xsd:anyURI.
  NI
412 : SUB CONSTRAINT: The URI in the "uri" attribute of a <reference> element MAY be extended by a media fragment.
  NI
413 : The <reference> element MAY contain a "role" attribute.
  NI
414 : The value of the "role" attribute of the <reference> element, if present, MUST be one of "expressedBy", "experiencedBy", "triggeredBy", "targetedAt".
  NI
415 : The <reference> element MAY contain a "media-type" attribute.
  NI
416 : The value of the "media-type" attribute of the <reference> element, if present, MUST be of type xsd:string.
  NI
417 : SUB CONSTRAINT: The value of the "media-type" attribute of the <reference> element, if present, MUST be a valid MIME type.
  NI
420 : The value of the "start" attribute of <emotion>, if present, MUST be of type xsd:nonNegativeInteger.
  NI
421 : The value of the "end" attribute of <emotion>, if present, MUST be of type xsd:nonNegativeInteger. 
  NI
422 : The value of "duration" attribute of <emotion>, if present, MUST be of type xsd:nonNegativeInteger.
  NI
423 : The value of the "time-ref-uri" attribute of <emotion>, if present, MUST be of type xsd:anyURI.
  NI
424 : The value of the "time-ref-anchor-point" attribute of <emotion>, if present, MUST be either "start" or "end".
  NI
425 : The value of the "offset-to-start" attribute of <emotion>, if present, MUST be of type xsd:integer.
  NI

Scale values
--------------
500 : The value of a "value" attribute, if present, MUST be a floating point value from the closed interval [0, 1].
  pass
501 : The <trace> element MUST have a "freq" attribute.
  NI
502 : The value of the "freq" attribute of <trace> MUST be a positive floating point number followed by optional whitespace followed by "Hz".
  NI
503 : The <trace> element MUST have a "samples" attribute.
  NI
504 : The value of the "samples" attribute of <trace> MUST be a space-separated list of floating point values from the closed interval [0, 1].
  NI

Defining vocabularies for representing emotions
-------------------------------------------------
600 : A <vocabulary> element MUST contain one or more <item> elements.
  pass
601 : A <vocabulary> element MAY contain a single <info> element.
  NI
602 : A <vocabulary> element MUST contain a "type" attribute.
  pass
603 : The value of the "type" attribute of the <vocabulary> element MUST be one of "category", "dimension", "action-tendency" or "appraisal".
  pass
604 : A <vocabulary> element MUST contain an "id" attribute
  pass
605 : The value of the "id" attribute of the <vocabulary> element MUST be of type xsd:ID .
  pass
606 : An <item> element MAY contain a single <info> element.
  NI
607 : An <item> element MUST contain a "name" attribute.
  pass
608 : An <item> MUST NOT have the same name as any other <item> within the same <vocabulary>.
  pass

Conformance
---------------
700 : All EmotionML elements MUST use the EmotionML namespace, "http://www.w3.org/2009/10/emotionml".
  pass

Issues
==========

* The the size of the vocabulary we use is larger than most state-of-the-art
  approaches to affective computing. Nevertheless, the ``vocabulary`` idiom of
  EmotionML is adequate to enable our atypical approach. Calling an item of
  such a large vocabulary a "category" is slightly misleading, but another
  word that is more appropriate does not come to mind.

* Multi-word vocabulary items, like "let down" are not valid according to
  xs:NMTOKEN

* The producer and consumer of EmotionML in this application is the same
  program.  The use of EmotionML is to persist dyanmic components of the
  EMO20Q questioner agent's state across HTTP requests.  Since the producer
  and consumer are the same program, a simple serialization of the agent's
  components would suffice.  However, the standardized format will be more
  useful in planned future developments that will require more heterogeneous
  system components: logging dialog information, visualization, and the case
  where the agent is a javascript object communicating via AJAX.
