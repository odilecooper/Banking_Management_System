DROP database lab3;
create database lab3;

use lab3;

# DROP table Cli_Debt;
# DROP table Debts_pay;
# DROP table Debts;
# DROP table Cli_Acc;
# DROP table Accounts;
# DROP table Clients;
# DROP table Assistants;
# DROP table Banks;

create table Banks (
    bank_name varchar(20) primary key,
    city varchar(10)
);
create table Assistants (
    id char(18) primary key,
    bank_name varchar(20),
    Constraint fkAssist_bank_name foreign key(bank_name) references Banks(bank_name),
    pos int, # 0=normal, 1=manager
    name varchar(10),
    tel char(11),
    addr varchar(30),
    sec_num int,
    sec_type int,
    sec_mng_id char(18), # fk?
    work_date date
);
create table Clients (
    id char(18) primary key,
    name varchar(10),
    tel char(11),
    addr varchar(50),
    con_name varchar(10),
    con_tel char(11),
    con_email varchar(50),
    con_relat varchar(10),
    assist_id char(18),
    Constraint fkCli_assist_id foreign key(assist_id) references Assistants(id)
);
create table Accounts (
    acc_num int auto_increment,
    bank_name varchar(20),
    Constraint fkAcc_bank_name foreign key(bank_name) references Banks(bank_name),
    balance float,
    open_date date,
    visit_date date,
    acc_type varchar(10),
    
    Constraint pk_Accounts primary key(acc_num)
);
create table Save_accounts (
    acc_num int primary key,
    Constraint fkSave_acc_num foreign key(acc_num) references Accounts(acc_num),
    int_rate float,
    cur_type int
);
create table Check_accounts (
    acc_num int primary key,
    Constraint fkCheck_acc_num foreign key(acc_num) references Accounts(acc_num),
    overdraft float
);
create table Cli_Acc (
    cli_id char(18),
    Constraint fkCA_cli_id foreign key(cli_id) references Clients(id),
    acc_num int,
    Constraint fkCA_acc_num foreign key(acc_num) references Accounts(acc_num),

    Constraint pk_Cli_Acc primary key(cli_id, acc_num)
);
create table Cli_Bank_Acctype (
    cli_id char(18),
    Constraint fkCBA_cli_id foreign key(cli_id) references Clients(id),
    bank_name varchar(20),
    Constraint fkCBA_bank_name foreign key(bank_name) references Banks(bank_name),
    acc_num int,
    Constraint fkCBA_acc_num foreign key(acc_num) references Accounts(acc_num),
    acc_type varchar(10),

    Constraint pk_Cli_Acc primary key(cli_id, bank_name, acc_type)
);
create table Debts (
    debt_num int auto_increment,
    bank_name varchar(20),
    Constraint fkDeb_bank_name foreign key(bank_name) references Banks(bank_name),
    amount float,
    paid_amount float,
    
    Constraint pk_Debts primary key(debt_num)
);
create table Debts_pay (
    debt_num int,
    Constraint fkDp_debt_num foreign key(debt_num) references Debts(debt_num),
    pay_date date,
    pay_sum float,

    Constraint pk_Debts_pay primary key(debt_num, pay_date)
);
create table Cli_Debt (
    cli_id char(18),
    Constraint fkCD_cli_id foreign key(cli_id) references Clients(id),
    debt_num int,
    Constraint fkCD_debt_num foreign key(debt_num) references Debts(debt_num),

    Constraint pk_Cli_Debt primary key(cli_id, debt_num)
);

insert into Banks value ("bname1", "city1");
insert into Banks value ("bname2", "city2");
insert into Banks value ("bname3", "city3");

insert into Assistants value
    ("001", "bname1", 1, "aname1", "11111111111", "addr1", 1, 1, "001", "2020-01-01");
insert into Assistants value
    ("002", "bname1", 0, "aname2", "22222222222", "addr2", 1, 1, "001", "2020-01-02");
insert into Assistants value
    ("003", "bname1", 0, "aname3", "33333333333", "addr3", 1, 1, "001", "2020-01-03");
insert into Assistants value
    ("004", "bname2", 1, "aname4", "44444444444", "addr4", 2, 2, "004", "2020-01-04");
insert into Assistants value
    ("005", "bname2", 0, "aname5", "55555555555", "addr5", 2, 2, "004", "2020-01-05");
insert into Assistants value
    ("006", "bname2", 0, "aname6", "66666666666", "addr6", 2, 2, "004", "2020-01-06");
insert into Assistants value
    ("007", "bname3", 1, "aname7", "77777777777", "addr7", 3, 1, "007", "2020-01-07");
insert into Assistants value
    ("008", "bname3", 0, "aname8", "88888888888", "addr8", 3, 1, "007", "2020-01-08");
