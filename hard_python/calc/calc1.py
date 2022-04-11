from tkinter import *
import re


def validate_input():
    r1 = re.match('^[+-]?[\d]+[.]?[\d]*$', op1.get())
    r2 = re.match('^[+-]?[\d]+[.]?[\d]*$', op2.get())
    return r1 and r2


def cmd_math(ops):
    is_valid = validate_input()
    if(is_valid):
        op1_value = float(op1.get())
        op2_value = float(op2.get())

        if(ops == '+'):
            res = op1_value+op2_value
        elif(ops == '-'):
            res = op1_value-op2_value
        elif(ops == 'x'):
            res = op1_value*op2_value
        elif(ops == '/'):
            res = op1_value/op2_value
        elif(ops == '%'):
            res = op1_value % op2_value
        elif(ops == '//'):
            res = op1_value//op2_value
        elif(ops == '**'):
            res = op1_value**op2_value
        res_var.set(round(res, 2))
    else:
        res_var.set('输入不合法')


def clear():
    op1.delete(0, END)
    op2.delete(0, END)
    res_var.set('Show Result')


# f2的计算方法
def calc_art():
    ex = op_art.get()
    if(re.match('[\w]+', ex)):
        res_str.set('输入非法')
    else:
        res = eval(ex)
        res_str.set(res)
    

root = Tk()  # 创建根窗口

menubar = Menu(root)
menu1 = Menu(menubar)
menu1.add_command(label='普通', command=lambda: f1.tkraise())
menu1.add_command(label='文艺', command=lambda: f2.tkraise())
menubar.add_cascade(label='模式', menu=menu1)
root.config(menu=menubar)

f1 = Frame(root)
f1.grid(row=0, column=0, sticky='news')

# 1.创建组件，创建组件的时候一定要指定组件所在的容器
op1_text = Label(f1, text='操作数1')
op2_text = Label(f1, text='操作数2')
op1 = Entry(f1)
op2 = Entry(f1)
btn_add = Button(f1, text='+', padx=50, pady=10,
                 command=lambda: cmd_math('+'))
btn_sub = Button(f1, text='-', padx=50, pady=10,
                 command=lambda: cmd_math('-'))
btn_mul = Button(f1, text='x', padx=50, pady=10,
                 command=lambda: cmd_math('x'))
btn_div = Button(f1, text='/', padx=50, pady=10,
                 command=lambda: cmd_math('/'))
btn_mod = Button(f1, text='%', padx=50, pady=10,
                 command=lambda: cmd_math('%'))
btn_flo = Button(f1, text='//', padx=50, pady=10,
                 command=lambda: cmd_math('//'))
btn_exp = Button(f1, text='**', padx=50, pady=10,
                 command=lambda: cmd_math('**'))
btn_clr = Button(f1, text='clear', padx=50, pady=10, command=clear)
res_var = StringVar()
res_var.set('Show Result')
result = Label(f1, textvariable=res_var, pady=20)

# 2.把组件显示出来
op1_text.grid(row=0, column=0, sticky='WE')
op2_text.grid(row=1, column=0, sticky='WE')
op1.grid(row=0, column=1, columnspan=3, sticky='WE')
op2.grid(row=1, column=1, columnspan=3, sticky='WE')
btn_add.grid(row=2, column=0, sticky='WE')
btn_sub.grid(row=2, column=1, sticky='WE')
btn_mul.grid(row=2, column=2, sticky='WE')
btn_div.grid(row=2, column=3, sticky='WE')
btn_mod.grid(row=3, column=0, sticky='WE')
btn_flo.grid(row=3, column=1, sticky='WE')
btn_exp.grid(row=3, column=2, sticky='WE')
btn_clr.grid(row=3, column=3, sticky='WE')
result.grid(row=4, column=0, columnspan=4, sticky='WE')

# f2第二种计算模式
f2 = Frame(root)
f2.grid(row=0, column=0, sticky='news')
op_art = Entry(f2)
btn_art = Button(f2, text='计算', command=calc_art)
res_str = StringVar()
res_str.set('Show Result')
Label_art = Label(f2, textvariable=res_str)
op_art.pack(fill=BOTH)
btn_art.pack(fill=BOTH)
Label_art.pack(fill=BOTH)

mainloop()
