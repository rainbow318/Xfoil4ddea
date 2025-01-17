## 主要代码介绍
./callXfoil.py
* HicksHenne函数功能：根据输入的$\theta$计算其对应的机翼几何形状
* evaluate_foil函数功能：调用Xfoil软件，根据输入的机翼几何形状评估该机翼的升阻比
* main函数体：实现数据集采样，生成的数据集存在./data文件夹中。（实际上该过程应该封装成一个函数的，但现在懒得改了就先写在mian函数体里）

## DDEA 机翼应用流程
#### Step1.数据采集
采集用于DDEA优化的数据集（目标值为翼型数据所对应的升阻比），数据集形式：$$(\theta_1^1,\theta_2^1,...\theta_{10}^1, C_{L/D}^1 ),...,(\theta_1^n,\theta_2^n,...\theta_{10}^n, Fitness^n )$$
具体步骤：
1）lhs采样得到n组$\theta$
2）对每个$\theta$，基于HicksHenne函数计算其对应的机翼几何形状，输出几何形状文件.dat（Xfoil好像只能读取.dat类型的文件）。一个.dat文件的例子：
```
1.0 0.00126
0.993723 0.0021370278357203797
0.982775 0.0036524940393088978
0.969992 0.005406714096973532
0.955666 0.007369479618182957
0.940264 0.00950137463089086
```
3）将.dat文件导入XFoil评估$C_L$和$C_D$，计算得到升阻比$C_{L/D}$。计算命令：
```
> load myfoil.dat
> norm
> oper
> iter 100
> mach 0.5
> visc 5000000
> alfa 4
> pacc
> output.txt
> alfa 4
```
4）根据文件output.txt（内含$C_L$和$C_D$），计算升阻比$C_{L/D}=\frac{C_L}{C_D}$。一个output.txt的具体例子：
```
       XFOIL         Version 6.99
  
 Calculated polar for:                                                 
  
 1 1 Reynolds number fixed          Mach number fixed         
  
 xtrf =   1.000 (top)        1.000 (bottom)  
 Mach =   0.500     Re =     5.000 e 6     Ncrit =   9.000
  
   alpha    CL        CD       CDp       CM     Top_Xtr  Bot_Xtr
  ------ -------- --------- --------- -------- -------- --------
   4.000   0.6292   0.00614   0.00193  -0.0080   0.2187   0.7294
```


如果不想手动进行上述1234的过程，也可以直接使用callXfoil.py的main函数体部分生成数据集。生成的runtime个数据集会存在./data文件夹中，i_eta.npy是第i次实验的所有决策变量，i_Cld.npy是第i次实验的各个决策变量所对应的目标函数值
#### Step2. DDEA优化
DDEA基于数据集进行数据驱动的优化，得到一个final翼型解，其形式为：
$$\theta_1^{best},\theta_2^{best},...\theta_{10}^{best}$$

#### Step3. 评估DDEA的解
如果是手动计算的话，和Step1差不多，先根据HicksHenne函数计算$\theta^{best}$对应的机翼几何形状，然后将形状输入到Xfoil中计算升阻比。

如果不想手动打开Xfoil并输入命令，评估机翼也可以通过CallXfoil.py中的evaluate_foil函数直接计算。

#### Step4. 获取机翼曲面各处的压力
手动打开XFoil软件（也可以不用手动操作软件而是用代码，可类似地参考CallXfoil.py的实现），导入myfoil.dat，获取该翼型该翼型曲面各处的$C_P$压力。直接使用python画图得到压力系数图x-$C_P$。获取$x-C_p$的命令：
```
> load myfoil.dat  # 导入机翼横截面几何形状的数据
> norm
> oper
> iter 100        # 设置Xfoil评估机翼性能的迭代次数（理论上iter越大，Xfoil评估该机翼越准确）
> mach 0.5         # 环境参数
> visc 5000000     # 环境参数
> alfa 4           # 环境参数
> cpwr ans.txt     # x-Cp数据输出到ans.txt文件中，随后使用python解析ans.txt文件并画图
```

x-Cp数据输出到ans.txt文件中，一个ans.txt的例子为：
```
 Alfa =   4.00000 Re =  5000000.000 Xflap,Yflap =     0.000000    0.000000
#    x        y        Cp  
   1.00000  0.00126  0.24861
   0.99372  0.00214  0.23505
   0.98277  0.00365  0.20910
   0.96999  0.00541  0.18260
...
```



