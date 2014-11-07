clear all;

% load in data, set up adjaceny matrix
x = importdata('../lists/features.txt');  %emotions vs questions
e = textread('../lists/emotions.txt','%s');  %list of emotions
q = textread('../lists/questions.txt','%s'); %list of questions

rm_qs_wo_ans = true;
rm_id_qs = true;

if rm_qs_wo_ans
x = x(:,find(sum(abs(x))>0));
q = q(find(sum(abs(x))>0));
end
if rm_id_qs
ind = regexpcell(q,'^e==');
[val,ind] = setdiff(q,q(ind));
q=q(ind);
x=x(:,ind);
end
index = [e;q];  %all indexes to the adjacency matrix

e_new=e;
lastQuestion=[];
lastQuestionIdx=[];
num_q=1;

while(num_q<=20 && length(e_new)>1)
    num_q=num_q+1;
    A = [zeros(size(x,1)) x; x' zeros(size(x,2))];  %adjaceny matrix
    %A(find(A<0))=0;
    A = abs(A);   %make it the absolute adjacency matrix
    
    %get initial ranking
    rank = pagerank(index,A);   %Cleve Moler's pagerank implementation with default settings
    [val,ind] = sort(rank,'descend');
    rankedIndex = index(ind);
    
    %remove emotions from ranking
    [val,ind] = setdiff(rankedIndex,e_new);
    rankedIndex = rankedIndex(sort(ind));
    %remove emotion identity questions (e.g., 'e==sadness')
    ind = regexpcell(rankedIndex,'^e==');
    [val,ind] = setdiff(rankedIndex,rankedIndex(ind));
    rankedIndex = rankedIndex(sort(ind));
    [val,ind] = setdiff(rankedIndex,lastQuestion);
    rankedIndex = rankedIndex(sort(ind));
    
    question = rankedIndex(1);
    lastQuestion = [lastQuestion;question];
    
    questionIndex = find(strcmp(question,q));
    lastQuestionIdx = [lastQuestionIdx;questionIndex];
    
    answer(num_q) = input([cell2mat(question),'? (y|n|m)\n'],'s');
    if answer(num_q)=='y'
        answer_n(num_q)=1;
    elseif answer(num_q)=='n'
        answer_n(num_q)=-1;
    else
        answer_n(num_q)=0;
    end
end

A = [zeros(size(x,1)) x; x' zeros(size(x,2))];  %adjaceny matrix
A = abs(A);   %make it the absolute adjacency matrix
rank = pagerank(index,A);   %Cleve Moler's pagerank implementation with default settings
[val,ind] = sort(rank,'descend');
rankedIndex = index(ind);

[val,ind] = intersect(rankedIndex,e);
rankedEmotion = rankedIndex(sort(ind))
