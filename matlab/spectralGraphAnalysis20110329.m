x = importdata('../lists/features.txt');
e = importdata('../lists/emotions.txt');
q = importdata('../lists/questions.txt');
xx = x(:,2:end);
A = [zeros(size(xx,1)) xx; xx' zeros(size(xx,2))]
AA = abs(A)
D = diag(sum(AA))
L = D-AA
eig(L)
%doh, 28 eigenvalues == 0 
% I need to remove questions that have no yes/no answers:
x = importdata('lists/features.txt');
e = importdata('lists/emotions.txt');
q = importdata('lists/questions.txt');
%this is the step that removes the questions w/ 0 answers
x = x(:,find(sum(abs(x(:,2:end)))>0))
xx = x(:,2:end);
A = [zeros(size(xx,1)) xx; xx' zeros(size(xx,2))]
AA = abs(A)
D = diag(sum(AA))
L = D-AA
eig(L)

  %doh, still 23 zero eigenvalues: need to make rows into emotions
x = importdata('lists/features.txt');
e = importdata('lists/emotions.txt');
q = importdata('lists/questions.txt');
%this is the step that removes the questions w/ 0 answers
xx = x(:,find(sum(abs(x))>0))
A = [zeros(size(xx,1)) xx; xx' zeros(size(xx,2))]
AA = abs(A)
D = diag(sum(AA))
L = D-AA
eig(L)


