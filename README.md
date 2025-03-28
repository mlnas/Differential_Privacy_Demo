The right number of epochs depends on your goal:

🔍 Quick test / debug	1–5	Fast run, just to verify setup and output

🧪 Visualize accuracy vs epsilon	5–15	Shows tradeoff: more epochs = higher accuracy but higher ε

📊 Privacy budget focus	3–10	Keeps ε lower while showing some model learning

🎓 Training for real performance	15–30	Pushes accuracy up (but ε increases too)


📊 Final Results: DP vs Non-DP
Metric	Differentially Private Model	Baseline Model (No DP)
Accuracy	91.91%	97.86%
Privacy Budget (ε)	1.28	❌ None (public risk)
Noise Multiplier	1.1	N/A
Epochs	15	15
Dataset	MNIST	MNIST
🔍 Takeaway
You traded ~6% accuracy for strong privacy guarantee
(ε = 1.28).

This shows DP is practical — especially in settings like healthcare, finance, or user data apps where privacy is a must.