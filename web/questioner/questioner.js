// making ajax calls to couchdb :
// $ = require('jquery')
// $.ajax({url:'http://ark.usc.edu:5984/emo20q',type:'POST', contentType:"application/json", data:JSON.stringify({"fuck":"you"})}).done(function(msg){console.log(msg)})
if(!Array.prototype.last) {
    Array.prototype.last = function() {
        return this[this.length - 1];
    };
}

function QAgent(){
    this.counter = 0;
    this.matchNum = 0;
    this.turnNum = 0;
    this.episodicBuffer = [];
    this.repl = QAgent.prototype.initialState;
    this.state = "initialState";
    this.dialog = {
	"type":"HumanComputerDialog",
	"provenance":["web-js",'text','generation1'],
	"events":[]
    };
    this.remember( {"talker":"questioner-agent",
		    "type": "Utterance",
		    "utterance":"Please pick an emotion and let me know when you are ready."} );
    
    // this.db.get("_all_docs", 
    // 		function(input){ 
    // 		    console.log(input);
    // 		} );
}

QAgent.prototype.initialState = function(input){ 

    this.remember( {"talker":"user", 
		    "type":"Utterance",
		    "utterance": input });
    var tmp = this.nlpIsReady(input);
    var output;
    if(tmp){
	//create new match
	this.dialog.events.push({'type':'Match',
				 'turns':[]     });
	output = "great, let me think...\n";
	var tmp = this.pickNextQuestion();
	output = output + "\n" + tmp.surface;
	this.toAskingState();
    }else{
	output = "let me know when you are ready...";
    }

    
    this.remember( {"talker":"agent",
		    "role":"questioner",
		    "utterance": output });

    //console.log(this.episodicBuffer);

    return output;
}; 

QAgent.prototype.askingState = function(input){ 
     if(this.turnNum == 0){ //when starting a new match
	this.matchNum++;
    }
    this.turnNum++; 
    var agloss = this.nlpClassifyYN(input);
    this.remember({"talker":"user",
		   "role":"answerer",
		   "utterance":input,
		   "agloss":agloss    });
    var output;
    if(agloss ==1){
	output = "you said 'yes'";
    }else if (agloss == -1){
	output = "you said 'no'";
    }else{
	output = "you said 'other'";
    }

    var tmp = this.pickNextQuestion();
    output = output + "\n" + tmp.surface;

    this.remember({"talker":"agent", 
		   "role":"questioner",
		   "utterance": output,
		   "qgloss" : tmp.qgloss });
    
   // console.log(this.episodicBuffer);

    return output;
}; 

QAgent.prototype.toAskingState = function(){
    this.state = "asking";
    this.repl = QAgent.prototype.askingState;
};

QAgent.prototype.pickNextQuestion = function(input){ 
    var tmp = {};
    tmp['surface'] = "Is it a stoopid emotion?";
    tmp['qgloss'] = "e==stupid";
    return tmp;

};
QAgent.prototype.remember = function(item){ 
    if(this.state=="asking"||this.state=="guessing"){
	this.episodicBuffer.push(item);
	if("talker" in item && item["talker"] == "agent"){
	    item["state"] = this.state;
	    this.dialog.events.last().turns.push(
  		{"type":"Turn", 'qa':[item]});
	    
	} else if("talker" in item && item.talker == "user"){
 	    this.dialog.events.last().turns.last().qa.push(item);
	}
    }else{
	this.dialog.events.push(item);	
    }

    console.log(this.dialog);
    
};



QAgent.prototype.nlpIsReady = function(input){
    return  /\byes\b|\bready\b|\bsure\b|\bgo\b|\bok\b|\bokay\b/.test(input);
};
QAgent.prototype.nlpClassifyYN = function(input){
    if(/\byes\b|\byeah\b|\byea\b|\byep\b|\baye\b|\bsure\b|\byup\b/.test(input)){
	return 1;
    }else if(/\bno\b|\bnope\b|\bnah\b/.test(input)){
	return -1;
    }else{
	return 0;
    }
};
QAgent.prototype.nlpIsAffirmative = function(input){
   if(this.nlpClassifyYN(input) == 1){
       return true;
   }else{
       return false;
   }
};

QAgent.prototype._eval = QAgent.prototype.nlpClassifyYN;

//var questioner = new QAgent();


// detect node vs browser
// cf http://stackoverflow.com/questions/4224606/how-to-check-whether-a-script-is-running-under-node-js
(function () {

     // Establish the root object, `window` in the browser, or `global` on the server.
     var root = this; 
     
     // Create a refeence to this
     var questioner = new QAgent();
     
     root.isNode = false;

    // Export the questioner object for **CommonJS**, with backwards-compatibility
    // for the old `require()` API. If we're not in CommonJS, add `questioner` to the
    // global object.
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = questioner;
        root.isNode = true;
	console.log("it's node.js");
        root.questioner = questioner;
	process.stdin.setEncoding('utf8');
	var stdin = process.openStdin();
	console.log("Please pick an emotion and let me know when you are ready.");
	stdin.on('data', function(chunk) { 
		     chunk = chunk.replace(/(\r\n|\n|\r)$/,"");
		     console.log(questioner.repl(chunk)); 
		 }
		);

    } else {
	console.log("it's NOT node.js");
        root.questioner = questioner;

    }
})();
