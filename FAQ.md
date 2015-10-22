# What? #

Emotion twenty questions (emo20q) is a game to study _natural language descriptions of emotions_ in the social context of human dialog interaction.  _Natural language descriptions of emotions_ (NLDE) are definite descriptions that refer to the subjective, theoretical entities known as emotions (according to Abe Kazemzadeh's PhD thesis, _in progress_).  As one way to study NLDE, we use a game like the familiar twenty questions game, except that the answerer (the player whose current role is to answer the questions) must choose an emotion word instead of an arbitrary object.  To study this in an observable context, we use an XMPP chat server as a playing field and a message logger to record the games.

# Why? #

  * Why not.

  * I had to pick a topic for my Ph.D. dissertation that was 1) novel, 2) theoretically interesting, 3) empirically verifiable, 4) computationally implementable, and 5) fun.

  * the study of emotions benefits from experimental frameworks that help to better observe the phenomena of emotions from different angles.  I identified the theoretical/abstract descriptions of emotions in the context of natural language communication as a area where existing experimental techniques were lacking.  By "theoretical/abstract" descriptions of emotions I mean when people describe emotions abstractly, as opposed to expressing their own emotions.  This is useful when people describe past emotions that they are not currently experiencing (a.k.a., emotion self report) and when they make explanations and theories about emotions.  Most existing experimental techniques have focused on when people describe their own, current emotion (as in sentiment analysis) while this focuses on the ability of people to introspect on what an emotion is and how they can be described.


# Why google code/open source? #

  * Even though this is an academic project that deals primarily with data being used to verify abstract ideas, it includes some code.  Moreover, I feel the open source methodology has much in common with the scientific method.  In particular I think that the goals of the open source movement align particularly well with aiding reproducibility of experiments and allowing others to build on previous work.

# Why GPLv3 and CC-BY-SA? #

  * I intend for GPLv3 to apply to the code and CC-BY-SA to apply to the data generated from the game.  GPL ensures that any improvements to the code are shared with the community.  For code involving ejabberd, this is required because ejabberd is also GPLed (currently I have no modifications of my own for ejabberd, but I use a community provided plug-in that allows the IM messages to be logged) and for other code, this will allow others to make use of scripts that are needed to analyze the data.  CC-BY-SA is the Creative Commons license for share-alike with attribution.  This makes it like the GPL for data and allows me to get cited when people use my work, a common academic practice.