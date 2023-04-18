from epic import *;
epic.start();

Logger.setLevel(Logger.Level.INFO);

System.out.println("="*10 + "\n" + "Calculator" + "\n" +  "="*10);

while true:
    System.out.println("[1] Addition");
    System.out.println("[2] Subtraction");
    System.out.println("[3] Multiplication");
    System.out.println("[4] Division");
    System.out.println("[5] Exit");

    choice = System.stdin.nextLine("Enter your choice: ");

    if choice == '5':
        break;

    num1 = float(System.stdin.nextLine("Enter first number: "));
    num2 = float(System.stdin.nextLine("Enter second number: "));

    if choice == '1':
        result = num1 + num2;
        operation = "+";
    elif choice == '2':
        result = num1 - num2;
        operation = "-";
    elif choice == '3':
        result = num1 * num2;
        operation = "*";
    elif choice == '4':
        result = num1 / num2;
        operation = "/";
    else:
        System.out.println("Invalid input\n");
        continue;

    System.out.println(String.format("%s %s %s = %s\n", num1, operation, num2, result));
