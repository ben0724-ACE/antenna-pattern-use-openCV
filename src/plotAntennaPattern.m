% 读取CSV文件
data = readtable('antenna_data.csv');

% 提取数据
angles = data.Time_s_;  % 角度数据
power_V = data.Power_V_dBm_;  % 垂直极化功率数据
power_H = data.Power_H_dBm_;  % 水平极化功率数据

% 将角度转换为弧度
angles_rad = deg2rad(angles * (360/36));  % 转换为0-360度，然后转为弧度

% 创建新的图形窗口
figure('Position', [100, 100, 800, 800]);

% 创建极坐标图
polarplot(angles_rad, power_V, 'b-', 'LineWidth', 2);
hold on;
polarplot(angles_rad, power_H, 'r-', 'LineWidth', 2);

% 设置图形属性
rlim([-70 30]);  % 设置径向范围
rticks([-70:10:30]);  % 设置径向刻度
rticklabels({'-70dBm','-60dBm','-50dBm','-40dBm','-30dBm','-20dBm',...
             '-10dBm','0dBm','10dBm','20dBm','30dBm'});

% 设置方向（使0度指向北方，逆时针旋转）
set(gca, 'ThetaDir', 'clockwise');
set(gca, 'ThetaZeroLocation', 'top');

% 添加图例
legend('Vertical', 'Horizontal', 'Location', 'southoutside');

% 添加标题
title('Antenna Pattern');

% 添加网格
grid on;

% 保存图形
saveas(gcf, 'antenna_pattern_matlab.png');
