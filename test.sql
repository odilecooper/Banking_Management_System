use lab3;
insert into Clients value
    ("001", "name1", "00000000001", "addr1", 
    "con1", "00000000011", "001@e.com", "relat1", "001");
insert into Clients value
    ("002", "name'2", "00000000002", "addr2", 
    "con2", "00000000022", "002@e.com", "relat2", "002");
insert into Clients value
    ("003", "name3", "00000000003", "addr1", 
    "con3", "00000000033", "003@e.com", "relat1", "001");
insert into Clients value
    ("004", "name4", "00000000004", "addr2", 
    "con4", "00000000044", "004@e.com", "relat2", null);

insert into Accounts value
    (null, "bname1", 0.0, "2019-09-19", "2020-03-12", "save");
insert into Save_accounts value
    (1, 0.01, 1);
insert into Cli_Acc value
    ("001", 1);
insert into Cli_Bank_Acctype value
    ("001", "bname1", 1, "save");

insert into Accounts value
    (null, "bname1", 0.0, "2019-10-11", "2020-02-02", "save");
insert into Save_accounts value
    (2, 0.01, 2);
insert into Cli_Acc value
    ("002", 2);
insert into Cli_Acc value
    ("003", 2);
insert into Cli_Bank_Acctype value
    ("002", "bname1", 2, "save");
insert into Cli_Bank_Acctype value
    ("003", "bname1", 2, "save");

insert into Accounts value
    (null, "bname1", 0.0, "2019-11-02", "2020-03-03", "check");
insert into Check_accounts value
    (3, 100);
insert into Cli_Acc value
    ("001", 3);
insert into Cli_Bank_Acctype value
    ("001", "bname1", 3, "check");

insert into Accounts value
    (null, "bname2", -100, "2020-01-01", "2020-03-19", "check");
insert into Check_accounts value
    (4, 200);
insert into Cli_Acc value
    ("003", 4);
insert into Cli_Acc value
    ("004", 4);
insert into Cli_Bank_Acctype value
    ("003", "bname2", 4, "check");
insert into Cli_Bank_Acctype value
    ("004", "bname2", 4, "check");

insert into Debts value
    (null, "bname1", 100, 10);
insert into Debts_pay value
    (1, "2020-01-01", 10);
insert into Cli_Debt value
    ("001", 1);

insert into Debts value
    (null, "bname3", 100, 80);
insert into Debts_pay value
    (2, "2019-12-08", 50);
insert into Debts_pay value
    (2, "2020-04-08", 30);
insert into Cli_Debt value
    ("002", 2);
insert into Cli_Debt value
    ("003", 2);
