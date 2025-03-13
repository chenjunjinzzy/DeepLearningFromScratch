/*
功能：51单片机上的一个简单实时操作系统，模仿FreeRTOS的设计思想，易于扩展
编写日期：2023年10月10日
编写作者：xxx
*/

#include <reg51.h>
#include <intrins.h>

#define MAX_TASKS 5                  // 最大任务数
#define BUTTON_PIN P3_0            // 按键连接到P3.0口
#define LED_PIN P1_0               // LED连接到P1.0口

typedef void (*task_t)(void);        // 任务类型定义，指向函数的指针

typedef unsigned int StackType_t;     // 定义栈元素类型为unsigned int

typedef struct TaskControlBlock // 任务控制块结构体定义
{
    task_t taskFunction;             // 任务函数地址
    StackType_t *sp;                 // 任务栈指针
    StackType_t stack[128];          // 任务栈空间
} TaskControlBlock_t;

TaskControlBlock_t tasks[MAX_TASKS]; // 任务控制块数组
unsigned char currentTask = 0;        // 当前正在运行的任务索引

// 初始化系统时调用此函数，注册任务
void os_Init(task_t task0, task_t task1, task_t task2, task_t task3, task_t task4)
{
    unsigned char i;

    // 初始化所有任务的状态
    for (i = 0; i < MAX_TASKS; i++)
    {
        tasks[i].taskFunction = NULL; // 将每个任务的函数指针先指向NULL
        tasks[i].sp = NULL;           // 将每个任务的栈指针先指向NULL
    }

    // 登记用户定义的任务函数
    if (task0 != NULL) tasks[0].taskFunction = task0;
    if (task1 != NULL) tasks[1].taskFunction = task1;
    if (task2 != NULL) tasks[2].taskFunction = task2;
    if (task3 != NULL) tasks[3].taskFunction = task3;
    if (task4 != NULL) tasks[4].taskFunction = task4;

    currentTask = 0;                    // 初始化当前任务索引为0
}

// 初始化每个任务的栈，并保存SP
static void init_task_Stack(TaskControlBlock_t *task, task_t taskFunc)
{
    StackType_t *sp, *stk_bottom;

    stk_bottom = task->stack;          // 任务栈的底部
    sp = &task->stack[127];            // 栈顶指针设置为栈的最后一个元素

    // 8051单片机的堆栈是向下生长的，所以按照向下生长来模拟
    *sp-- = (StackType_t)taskFunc;      // 返回地址（即任务入口地址）

    // 保留堆栈的其他寄存器（此时模拟环境，堆栈中压入堆寄存器）
    *sp-- = 0x00;                      // PSW
    *sp-- = 0x00;                      // ACC
    *sp-- = 0x00;                      // B
    *sp-- = 0x00;                      // DPL
    *sp-- = 0x00;                      // DPH

    // R0-R7
    *sp-- = 0x07;
    *sp-- = 0x06;
    *sp-- = 0x05;
    *sp-- = 0x04;
    *sp-- = 0x03;
    *sp-- = 0x02;
    *sp-- = 0x01;
    *sp-- = 0x00;

    // 由于8051的堆栈向下生长，所以指向栈顶元素的地方减8字节就是SP
    task->sp = sp;
}

// 任务调度函数，用于在任务之间切换
void os_Scheduler(void)
{
    currentTask++;                      // 切换到下一个任务
    if (currentTask >= MAX_TASKS)     // 如果超出最大任务数，从头开始
        currentTask = 0;

    // 如果该任务是NULL任务，则跳过
    while (tasks[currentTask].taskFunction == NULL)
    {
        currentTask++;
        if (currentTask >= MAX_TASKS)
            currentTask = 0;
    }
}

// 在每次时钟中断向量表调用此函数
void tick_ISR(void) interrupt 1
{
    // 任务调度
    os_Scheduler();

    // 清除中断标志（具体时钟中断寄存器需要根据具体的单片机型号来设置）
    TH0 = 0xFC;
    TL0 = 0x18;
}

// 创建任务
void os_CreateTask(unsigned char taskIndex, task_t taskFunc)
{
    // 保存任务函数地址
    tasks[taskIndex].taskFunction = taskFunc;

    // 初始化任务栈
    init_task_Stack(&tasks[taskIndex], taskFunc);
}

// 任务函数示例
void task0(void)
{
    static unsigned char lastButtonState = 1; // 按键按下状态，默认未按下
    unsigned char currentButtonState;

    while (1)
    {
        currentButtonState = BUTTON_PIN;  // 读取按键状态
        // 检测按键是否按下
        if (currentButtonState == 0 && lastButtonState == 1)
        {
            LED_PIN = !LED_PIN;  // 切换LED状态
            _nop_();             // Add some delay to debounce the button
        }
        lastButtonState = currentButtonState; // 更新上次按键状态

        _nop_(); // 防止任务卡死
    }
}

void task1(void)
{
    while (1)
    {
        // This task does nothing
    }
}

// 初始化并启动操作系统
void main(void)
{
    // 硬件初始化
    TMOD = 0x01;  // 定时器0模式1
    // 初始化各任务栈
    os_CreateTask(0, task0);
    os_CreateTask(1, task1);

    EA = 1;     // 使能全局中断
    ET0 = 1;    // 使能定时器0中断

    TH0 = 0xFC; // 定时器0初值设置， 51单片机12MHz晶振，定时周期约为1ms
    TL0 = 0x18;
    TR0 = 1;    // 定时器0启动

    while (1)
    {
        // 切换到当前任务的堆栈并执行任务
        if (tasks[currentTask].taskFunction != NULL)
        {
            __asm
                MOV SP, _currentTask
                ACALL os_GetSP
                MOV SP, A
                RET                     // 返回栈顶，开始执行任务
    __endasm;
}
        else
        {
            os_Scheduler();                 // 调度到下一个任务
        }
    }
}

unsigned int os_GetSP(unsigned char taskIndex) __naked
{
    __asm
        MOV R0, DPL
        MOV A, _tasks + 4
        ADD A, R0
        ADD A, R0
        ADD A, #2
        MOV DPL, A
        MOV A, @A + DPL
        RET
    __endasm;
}
