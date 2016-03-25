from process_model import *
def main():
	# import and normalize data
	train_data, test_data = 'codetest_train.txt', 'codetest_test.txt'
	train_x, test_x, train_target = import_data(train_data, test_data)
	train_norm = normalize_data(train_x)
	test_norm = normalize_data(test_x)

	#use cross validation to split training data
	X_train, X_test, y_train, y_test = cross_validation.train_test_split(
		train_norm, train_target, test_size = 0.2)

	#to prevent overfitting, we first apply l1 regularization, and use AkaShooting algorithm
	loss_list = []
	w_list = []
	for i in range(-5, -2):
		Lambda = 10**i
		w = AkaShooting(X_train, y_train, Lambda)
	  	loss = compute_square_loss(X_test,y_test,w)
		loss_list.append(loss)
		w_list.append(w)
	#The smallest loss is 12.3 for lasso	
	  	# print loss

	# #we can also use l2 regularization to prevent overfitting, this takes SGD algorithm
	for i in range(-5, -2):
		Lambda = 10**i
		w, loss= stochastic_grad_descent(X_train, y_train, Lambda, num_iter = 10)
		loss = compute_square_loss(X_test,y_test,w)
		loss_list.append(loss)
		w_list.append(w)
	#The smallest loss is 16, which is worse than lasso.
		# print loss

	min_loss = min(loss_list)
	index = loss_list.index(min_loss)
	w_star = w_list[index]
	y_output = np.dot(test_norm, w_star)
	np.savetxt('y_test.txt', y_output, delimiter='\n')

if __name__ == "__main__":
    main()




