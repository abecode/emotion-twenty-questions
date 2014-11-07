% Run leave-one-link-out link prediction on emo20q data
% using eigenvalue rank reduction

clear all; clc;

x = dlmread('../lists/features.txt');  %emotions vs questions
e = textread('../lists/emotions.txt','%s');  %list of emotions
q = textread('../lists/questions.txt','%s'); %list of questions

rm_qs_wo_ans = true;
%rm_id_qs = false;
rm_id_qs = true;

if rm_qs_wo_ans
xx = x(:,find(sum(abs(x))>0));
q = q(find(sum(abs(x))>0));
x=xx;
end
if rm_id_qs
ind = regexpcell(q,'^e==');
[val,ind] = setdiff(q,q(ind));
q=q(ind);
x=x(:,ind);
end
index = [e;q];  %all indexes to the adjacency matrix

A = [zeros(size(x,1)) x; x' zeros(size(x,2))];  %adjaceny matrix
D = diag(sum(A));
L = D - A;  %laplacian matrix
 
for dim = [10,20,50,100,150,200];
%for dim = [60:3:130];
msg = sprintf('predicting using %d dimensions', dim);
disp (msg);
inds_nz = find(x~=0);
is_correct = zeros(1,length(inds_nz));

for i=1:length(inds_nz)
    y=x;
    y(inds_nz(i))=0;
    Ay = [zeros(size(y,1)) y; y' zeros(size(y,2))];  %adjaceny matrix
    Dy = diag(sum(Ay));
    Ly = Dy - Ay;  %laplacian matrix
    [U,S]=eig(Ay);
    Apred=U(:,1:dim)*S(1:dim,1:dim)*U(:,1:dim)'; %perform link prediction
    Apred=sign(Apred);
    
    
    ind_pred = find(Ay~=A);
    is_correct(i) = all(A(ind_pred)==Apred(ind_pred));
end

accuracy = sum(is_correct)/length(is_correct)

end
