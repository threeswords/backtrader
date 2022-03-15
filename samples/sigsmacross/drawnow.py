clc;clear
DeltaT = 0.0000001;
n = 1000000000; % 导弹最长运行时间100s
PositionA = [0,0];  % A的坐标
PositionB = [20,0]; % B的坐标
% V = randi(100); %速度为1~100个单位内的随机数
V = 200;    % V若是0-100，曲线画的太慢
a = atan(V*DeltaT/sqrt(2)/(V*DeltaT/sqrt(2)+20)); % 角度a1
disp('正在模拟测试中');
k = 0; % 用于画图，当循环次数达到500时画一个点

plot(PositionA(1),PositionA(2),'.k','MarkerSize',1);  % 画出导弹和B船所在的坐标，点的大小为1，颜色为黑色(k)，用小点表示
grid on;  % 打开网格线
hold on;  % 不关闭图形，继续画图
plot(PositionB(1),PositionB(2),'.k','MarkerSize',1);  % 画出导弹和B船所在的坐标，点的大小为1，颜色为黑色(k)，用小点表示
hold on;  % 不关闭图形，继续画图

axis([0 30 0 10])  % 固定x轴的范围为0-30  固定y轴的范围为0-10
for i=1:n
    PositionB = PositionB + [V*DeltaT/sqrt(2),V*DeltaT/sqrt(2)];
    a = atan(PositionB(2)-PositionA(2)) / (PositionB(1)-PositionA(1));
    PositionA = PositionA + [3*V*DeltaT*cos(a),3*V*DeltaT*sin(a)];
    k = k+1;
    if mod(k,500) == 0   % 每刷新500次时间就画出下一个导弹和B船所在的坐标  mod(m,n)表示求m/n的余数
        plot(PositionA(1),PositionA(2),'.k','MarkerSize',1);  % 画出导弹和B船所在的坐标，点的大小为1，颜色为黑色(k)，用小点表示
        hold on;  % 不关闭图形，继续画图
        plot(PositionB(1),PositionB(2),'.k','MarkerSize',1);  % 画出导弹和B船所在的坐标，点的大小为1，颜色为黑色(k)，用小点表示
        hold on;  % 不关闭图形，继续画图
        pause(0.001);  % 暂停0.001s后再继续下面的操作
    end    
    
    if (abs(sum(PositionA-PositionB))<0.01) & (sqrt(sum(PositionA.*PositionA))<=50) %当导弹和B船足够近且在导弹射程之内
        disp('导弹能击中');
        break;
    end
end    
disp('模拟测试完毕');
