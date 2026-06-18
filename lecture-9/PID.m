s = tf('s');
m = 1; b = 5; k = 10;
Gs = 1/(m*s^2 + b*s + k); % -> Mass Spring Damper
k_p = 5; k_d = 10; k_i = 0.2;

%% P Control Step response
sys = k_p * Gs;
T = feedback(sys, 1);
figure;
step(T);
title(sprintf('Step Response for P Control (k_p = %g)',k_p));

%% PD Control Step response
sys = (k_p + k_d * s) * Gs;
T = feedback(sys, 1);
figure;
step(T);
title(sprintf('Step Response for PD Control (k_p = %g, k_d = %g)',k_p, k_d));

%% PI Control Step response
sys = (k_p + k_i / s) * Gs;
T = feedback(sys, 1);
figure;
step(T);
title(sprintf('Step Response for PI Control (k_p = %g, k_i = %g)',k_p, k_i));

%% PID Control Step response
sys = (k_p + k_i/s + k_d * s) * Gs;
T = feedback(sys, 1);
figure;
step(T);
title(sprintf('Step Response for PID Control (k_p = %g, k_d = %g, k_i = %g)', k_p, k_d, k_i));

%% PID Tuning
[C, info] = pidtune(Gs, 'PID');
k_p = C.Kp; k_d = C.Kd; k_i = C.Ki;
figure;
sys = (k_p + k_i/s + k_d * s) * Gs;
T = feedback(sys, 1);
step(T);
title(sprintf('Step Response for PID Control post-tuning (k_p = %g, k_d = %g, k_i = %g)', k_p, k_d, k_i));