import sampling as sp
import HicksHenneBumpFunc.bumpfunctions as bf
import subprocess
import numpy as np
import os
import glob
import random

# 计算对应的HicksHenne曲线y值
def HicksHenne(xy_coor_u,xy_coor_l,eta,dim,output_y_path):
    bumpfunc=bf.bumpfunc()
    up_func=[0,1,2,3,4,5]   # bumpfunc的索引从0开始
    low_func=[6,7,8,9]
    f=open(output_y_path,'a')

    sorted_ind=np.argsort(xy_coor_u[:,0])[::-1]
    sorted_xy_coor=xy_coor_u[sorted_ind]
    for xy in sorted_xy_coor:
        x_value=xy[0]
        y_value=xy[1]
        s_u=0
        for i in up_func:
            s_u+=eta[i]*bumpfunc.f(i,x_value)   
        y_u=s_u+y_value       
        f.write(f'{x_value} {y_u}\n')

    sorted_ind=np.argsort(xy_coor_l[:,0])
    sorted_xy_coor=xy_coor_l[sorted_ind]
    for xy in sorted_xy_coor:
        x_value=xy[0]
        y_value=xy[1]
        s_l=0
        for i in low_func:
            s_l+=eta[i]*bumpfunc.f(i,x_value)
        y_l=s_l+y_value
        f.write(f'{x_value} {y_l}\n')
    f.close()

def evaluate_foil(foilname,M,Re,AoA,eta,n_iter,dim,ind,xy_u,xy_l,noise=False):
    """
    random_rows=np.random.choice(xy_u.shape[0],size=n,replace=False)
    s_xy_coor_u=xy_u[random_rows,:]
    # 为了能在下表面选中和上表面一样的点，需要先对下表面的数据进行从大到小的排序
    sorted_ind=np.argsort(xy_l[:,0])[::-1]
    s_xy_coor_l=xy_l[sorted_ind]
    s_xy_coor_l=s_xy_coor_l[random_rows,:]
    """
    s_xy_coor_u=xy_u
    s_xy_coor_l=xy_l
    if noise is True:   # 需要添加噪音
        for i in range(dim):
            eta[i]+=random.uniform(-0.001,0.001)
    HicksHenne(s_xy_coor_u,s_xy_coor_l,eta,dim,output_y_path=foilname)
    command=f'load\n{foilname}\n\nnorm\noper\niter {n_iter}\nmach {M}\nvisc {Re}\nalfa {AoA}\npacc\n.\\eva_ret\\eva_{ind}.txt\n\n'
    command+=f'alfa {AoA}\n\n\n\nquit\n'
    process=subprocess.Popen([".\\FoilCal\\Xfoil\\xfoil.exe"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
    ret=process.communicate(input=command)[0]
    f=open(f'.\\eva_ret\\eva_{ind}.txt','r')
    lines=f.readlines()
    line=lines[-1]
    temp=line.split(' ')
    if temp[2]=='------':   # not converge
        # 从ret中寻找Cl和Cd，并计算C_ld
        cl_line=ret.splitlines()[-8].replace('\n','')
        cl=float(cl_line.split(' ')[-1])
        print(cl_line)
        print(cl)
        cd_lind=ret.splitlines()[-7]
        cd=float(cd_lind.split('=')[2].replace(' ',''))
        print(cd_lind)
        print(cd)
        return cl/cd
    
    cl=float(temp[6])
    cd=float(temp[9])
    #print(f'ind={ind} cl={cl} cd={cd}')
    if cd==0:
        return 0
    return cl/cd
    

# 函数返回上表面的(x_coordinate,y_coordinate)
def get_upper_lower_xy(M,Re,AoA,xy_path):
    command=f'naca0012\n\nnorm\noper\niter 100\nmach {M}\nvisc {Re}\nalfa {AoA}'
    command+=f'\n\n\nSAVE\n{xy_path}.txt\n\n\n'
    command+=f'quit\n'

    process=subprocess.Popen([".\\FoilCal\\Xfoil\\xfoil.exe"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
    ret=process.communicate(input=command)[0]
    #print(ret) # ret其实就是与xfoil交互的内容

    f=open(f'{xy_path}.txt','r')
    lines=f.readlines()

    xy_u=[]
    xy_l=[]
    for line in lines:
        if 'NACA' in line:
            continue
        temp=(line.replace('\n','')).split(' ')
        xy=[]
        for each in temp:
            if each!='':
                xy.append(float(each))
        #temp=[float(each) for each in temp]
        if xy[1]<0:
            xy_l.append(xy)
        else:
            xy_u.append(xy)
    xy_u=np.array(xy_u)
    xy_l=np.array(xy_l)
    path_u=f'{xy_path}_upper'
    path_l=f'{xy_path}_lower'
    np.save(path_u,xy_u)
    np.save(path_l,xy_l)
    return xy_u,xy_l

if __name__=='__main__':
    dim=10
    data_size=11*dim
    M=0.5
    Re=5*(10**6)
    AoA=4 #4°
    n_iter=100
    n=50    # 每次从x_coordinate中采样的点的个数
    lower_bound=[-0.001,-0.006,-0.009,-0.009,-0.006,-0.002,-0.001,-0.007,-0.007,-0.002]
    upper_bound=[0.001,0.006,0.009,0.009,0.006,0.002,0.001,0.007,0.007,0.002]
    for r in range(20):
        etas=sp.lhs(data_size,dim,lower_bound,upper_bound)
        np.save(f'.\\data\\{r}_eta.npy',etas)
        xy_path='.\\points'
        xy_u,xy_l=get_upper_lower_xy(M,Re,AoA,xy_path)   # xy_u为上表面的coordinate


        foilname=f'.\\myfoil\\myfoil'
        # 对etas，评估每组eta所对应的foil的C_ld

        c_ld=[evaluate_foil(f'{foilname}{i}.dat',M,Re,AoA,etas[i],n_iter,dim,i,xy_u,xy_l) for i in range(etas.shape[0])]
        c_ld=np.array(c_ld)
        np.save(f'.\\data\\{r}_Cld.npy',c_ld)

        files=glob.glob(os.path.join('.\\myfoil','*'))
        for file in files:
            os.remove(file)
        files=glob.glob(os.path.join('.\\eva_ret','*'))
        for file in files:
            os.remove(file)
        
