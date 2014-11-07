% load in data, set up adjaceny matrix

x = dlmread('../lists/features.txt');  %emotions vs questions
e = textread('../lists/emotions.txt','%s');  %list of emotions
q = textread('../lists/questions.txt','%s'); %list of questions
index=[e;q];
A = [zeros(size(x,1)) x; x' zeros(size(x,2))];  %adjaceny matrix


t = 'considering only positive edges for now ';
disp(t);
% negative edges to zero
A(find(A<0))=0;
%set up laplacian matrix, do eigenvalue decomposition
D = diag(sum(A));
L = D - A;
[v,lambda] = eig(L);
disp('the number of zero eigenvalues is the number of separate graph components');
l = length(find(diag(lambda)<.00000000001))
le = length(e);
% plot 3 dimensions from the 3 lowest eigenvalues
figure;
plot3(v(1:le,l+1),v(1:le,l+2),v(1:le,l+3),'*');
text(v(1:le,l+1),v(1:le,l+2),v(1:le,l+3),e);
title(t);


t='considering only positive edges, ignoring questions with no definite answers';
disp(t);
xx = x(:,find(sum(abs(x))>0));
A = [zeros(size(xx,1)) xx; xx' zeros(size(xx,2))];
% set negative edges to zero
A(find(A<0))=0; 
%set up laplacian matrix, do eigenvalue decomposition
D = diag(sum(A));
L = D - A;
[v,lambda] = eig(L);
disp('the number of zero eigenvalues is the number of separate graph components');
l = length(find(diag(lambda)<.00000000001))
le = length(e);
% plot 3 dimensions from the 3 lowest eigenvalues
figure;
plot3(v(1:le,l+1),v(1:le,l+2),v(1:le,l+3),'*');
text(v(1:le,l+1),v(1:le,l+2),v(1:le,l+3),e);
title(t);


t='now considering any yes/no edges';
disp(t);
A = [zeros(size(x,1)) x; x' zeros(size(x,2))];  %adjaceny matrix
%make it the absolute adjacency matrix
A=abs(A);
%set up laplacian matrix, do eigenvalue decomposition
D = diag(sum(A));
L = D - A;
[v,lambda] = eig(L);
disp('the number of zero eigenvalues is the number of separate graph components');
l = length(find(diag(lambda)<.00000000001))
le = length(e);
% plot 3 dimensions from the 3 lowest eigenvalues
figure;
plot3(v(1:le,l+1),v(1:le,l+2),v(1:le,l+3),'*');
text(v(1:le,l+1),v(1:le,l+2),v(1:le,l+3),e);
title(t);


t='considering any yes/no edges, ignoring questions with no definite answers';
disp(t);
xx = x(:,find(sum(abs(x))>0));
A = [zeros(size(xx,1)) xx; xx' zeros(size(xx,2))];
%make it the absolute adjacency matrix
A=abs(A);
% set negative edges to zero
%A(find(A<0))=0; 
%set up laplacian matrix, do eigenvalue decomposition
D = diag(sum(A));
L = D - A;
[v,lambda] = eig(L);
disp('the number of zero eigenvalues is the number of separate graph components');
l = length(find(diag(lambda)<.00000000001))
le = length(e);
% plot 3 dimensions from the 3 lowest eigenvalues
figure;
plot3(v(1:le,l+1),v(1:le,l+2),v(1:le,l+3),'*');
text(v(1:le,l+1),v(1:le,l+2),v(1:le,l+3),e);
title(t) ;


