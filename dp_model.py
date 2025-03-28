import tensorflow as tf
from tensorflow_privacy.privacy.optimizers.dp_optimizer_keras import DPKerasSGDOptimizer
from tensorflow_privacy.privacy.analysis import compute_dp_sgd_privacy
import numpy as np

# Load and preprocess MNIST
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
x_train = x_train.reshape(-1, 784).astype(np.float32)
x_test = x_test.reshape(-1, 784).astype(np.float32)

# ⚠️ Make sure training size is divisible by batch_size
batch_size = 256
num_microbatches = 256  # Must divide batch_size
epochs = 15
learning_rate = 0.25
l2_norm_clip = 1.0
noise_multiplier = 1.1

# Trim training set to a multiple of batch_size
num_batches = len(x_train) // batch_size
x_train = x_train[:num_batches * batch_size]
y_train = y_train[:num_batches * batch_size]

# ✅ Build DP optimizer
optimizer = DPKerasSGDOptimizer(
    l2_norm_clip=l2_norm_clip,
    noise_multiplier=noise_multiplier,
    num_microbatches=num_microbatches,
    learning_rate=learning_rate
)

# ✅ Build model
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(784,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
])

# ✅ Use unreduced loss (needed for DP)
loss = tf.keras.losses.SparseCategoricalCrossentropy(
    from_logits=True,
    reduction=tf.keras.losses.Reduction.NONE
)

model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

# ✅ Train with a tf.data.Dataset (drop incomplete batches)
train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
train_dataset = train_dataset.shuffle(10000).batch(batch_size, drop_remainder=True)

# 🏃‍♂️ Train
model.fit(train_dataset, epochs=epochs)

# ✅ Evaluate
loss_val, acc_val = model.evaluate(x_test, y_test)
print(f"\n✅ DP Model Accuracy: {acc_val:.4f}")

# ✅ Report ε
compute_dp_sgd_privacy.compute_dp_sgd_privacy(
    n=len(x_train),
    batch_size=batch_size,
    noise_multiplier=noise_multiplier,
    epochs=epochs,
    delta=1e-5
)
