%this script infers the relationship between a question and each emotion by
%calculating the sign of the product of the shortest path between the given
%question and emotion nodes in the unsigned graph
clear all; clc;

x = dlmread('../lists/features.txt');  %emotions vs questions
e = textread('../lists/emotions.txt','%s');  %list of emotions
q = textread('../lists/questions.txt','%s'); %list of questions

x = x(:,find(sum(abs(x))>0));
q = q(find(sum(abs(x))>0));
ind = regexpcell(q,'^e==');
[val,ind] = setdiff(q,q(ind));
q=q(ind);
x=x(:,ind);
index = [e;q];

A = [zeros(size(x,1)) x; x' zeros(size(x,2))];  %adjaceny matrix
Gsigned = sparse(A);
G = abs(Gsigned);

[dist,path,pred] = graphshortestpath(G,find(strcmp(index,'happiness')));%path to 'e.valence==positive'

for i=1:42
    path_i = path{i};
    sign(i)=1;
    for j=1:length(path_i)-1
        sign(i) = sign(i)*A(path_i(j),path_i(j+1));
    end
end

e_valence = [e';num2cell(sign)]'

%%%%%%%%%%%Output%%%%%%%%%%%%
% e_valence = 
%     'admire'           [ 1]
%     'adore'            [ 1]
%     'amusement'        [ 1]
%     'anger'            [-1]
%     'anxiety'          [-1]
%     'awe'              [ 1]
%     'boredom'          [-1]
%     'bravery'          [ 1]
%     'calm'             [ 1]
%     'confidence'       [ 1]
%     'confusion'        [-1]
%     'contempt'         [-1]
%     'depression'       [-1]
%     'devastated'       [-1]
%     'disgust'          [-1]
%     'enthusiasm'       [ 1]
%     'envy'             [-1]
%     'exasperated'      [-1]
%     'excitement'       [ 1]
%     'fear'             [-1]
%     'frustration'      [-1]
%     'glee'             [ 1]
%     'gratefulness'     [ 1]
%     'happiness'        [-1]
%     'hope'             [ 1]
%     'jealosy'          [-1]
%     'love'             [-1]
%     'melancholy'       [-1]
%     'pity'             [-1]
%     'proud'            [ 1]
%     'regret'           [-1]
%     'relief'           [ 1]
%     'sadness'          [-1]
%     'serenity'         [ 1]
%     'shame'            [-1]
%     'silly'            [ 1]
%     'soberness'        [ 1]
%     'surprise'         [-1]
%     'thankful'         [-1]
%     'thrilled'         [ 1]
%     'worry'            [ 1]
%     'worry/anxiety'    [-1]
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%