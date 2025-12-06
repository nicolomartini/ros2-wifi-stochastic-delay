%% Plot of the results of the simulation
close
clear
clc

% Data Extraction
load results.mat

%% Tracking Error Plots
nom.t = nominal.time;
nom.q = nominal.signals(1).values;
nom.q_meas = nominal.signals(2).values;
nom.q_ref = zeros(size(nom.q));
for i = 1:length(nom.t)
    nom.q_ref(i,:) = nominal.signals(3).values(:, :, i)';
end
nom.e = nom.q_ref - nom.q_meas;

net.t = networked.time;
net.q = networked.signals(1).values;
net.q_meas = networked.signals(2).values;
net.q_ref = zeros(size(net.q));
for i = 1:length(net.t)
    net.q_ref(i,:) = networked.signals(3).values(:, :, i)';
end
net.e = net.q_ref - net.q_meas;

% Empty Figure
figure('WindowState', 'maximized')

%% Nominal Control
subplot(211)
stairs(nom.t, nom.e, 'LineWidth', 3)
xlabel('t [s]', 'FontSize', 24)
ylabel('e [rad]', 'FontSize', 24)
title('Nominal Control', 'FontSize', 28)
legend('q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'FontSize', 20)
grid on
ax = gca;
ax.FontSize = 24;

%% Networked Control
subplot(212)
stairs(net.t, net.e, 'LineWidth', 3)
xlabel('t [s]', 'FontSize', 24)
ylabel('e [rad]', 'FontSize', 24)
title('Networked Control', 'FontSize', 28)
legend('q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'FontSize', 20)
grid on
axis([0, 2, -3, 3])
ax = gca;
ax.FontSize = 24;

% Global Title
sgtitle('Comparison of Tracking Errors', 'FontSize', 32);

%% Trajectory Plots
snapshotTime = 1.5;
t = nominal.time;
[~, idx] = min(abs(t - snapshotTime));
t_snapshot = t(idx);

nom.q_snap = nominal.signals(1).values(idx, :);
net.q_snap = networked.signals(1).values(idx, :);

% End Effector Trajectory Evaluation
nom.ee = zeros(idx, 3);
net.ee = zeros(idx, 3);
for i = 1:idx
    nom.traj = getTransform(robot, nom.q(i,:), 'tool0');
    nom.ee(i,:) = nom.traj(1:3,4)';
    net.traj = getTransform(robot, net.q(i,:), 'tool0');
    net.ee(i,:) = net.traj(1:3,4)';
end

% Empty Figure
fig = figure('WindowState', 'maximized');

%% Nominal Control
ax1 = subplot(1, 2, 1);
show(robot, nom.q_snap, 'PreservePlot', false, 'Frames', 'off', 'Parent', ax1);
hold(ax1, 'on');
grid(ax1, 'on');

% Handles for the Legend
h_ref1 = plot3(ax1, ref.x, ref.y, ref.z, '--', 'LineWidth', 3, 'Color', '#808080');
h_eff1 = plot3(ax1, nom.ee(:,1), nom.ee(:,2), nom.ee(:,3), 'LineWidth', 3, 'Color', '#0072BD');

% Graphic Settings
title(ax1, sprintf('Nominal Control [ t = %.2f s ]', t_snapshot), 'FontSize', 28);
xlim(ax1, [-0.5 0.5]); ylim(ax1, [-0.5 0.5]); zlim(ax1, [0 1]);
xlabel(ax1, ''); ylabel(ax1, ''); zlabel(ax1, '');
view(ax1, 160, 40);
camzoom(ax1, 0.9);
lighting(ax1, 'gouraud');
camlight(ax1, 'headlight');
ax = gca;
ax.FontSize = 24;
legend([h_ref1, h_eff1], {'Reference', 'Followed'}, 'Location', 'best', 'FontSize', 20);

%% Networked Control
ax2 = subplot(1, 2, 2);
show(robot, net.q_snap, 'PreservePlot', false, 'Frames', 'off', 'Parent', ax2);
hold(ax2, 'on');
grid(ax2, 'on');

% Handles for the Legend
h_ref2 = plot3(ax2, ref.x, ref.y, ref.z, '--', 'LineWidth', 3, 'Color', '#808080');
h_eff2 = plot3(ax2, net.ee(:,1), net.ee(:,2), net.ee(:,3), 'LineWidth', 3, 'Color', '#0072BD');

% Graphic Settings
title(ax2, sprintf('Networked Control [ t = %.2f s ]', t_snapshot), 'FontSize', 28);
xlim(ax2, [-0.5 0.5]); ylim(ax2, [-0.5 0.5]); zlim(ax2, [0 1]);
xlabel(ax2, ''); ylabel(ax2, ''); zlabel(ax2, '');
view(ax2, 160, 40);
camzoom(ax2, 0.9);
lighting(ax2, 'gouraud');
camlight(ax2, 'headlight');
ax = gca;
ax.FontSize = 24;
legend([h_ref2, h_eff2], {'Reference', 'Followed'}, 'Location', 'best', 'FontSize', 20);

% Global Title
sgtitle('Comparison of Followed Trajectories', 'FontSize', 32)
