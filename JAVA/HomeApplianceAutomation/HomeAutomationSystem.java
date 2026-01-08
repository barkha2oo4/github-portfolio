import java.io.*;
import java.util.*;

public class HomeAutomationSystem {
    private static final String FILE_NAME = "data/appliances.txt";

    public static void main(String[] args) {
        List<Appliance> appliances = loadAppliances();

        if (appliances.isEmpty()) {
            appliances.add(new Appliance("Light", false));
            appliances.add(new Appliance("Fan", false));
            appliances.add(new Appliance("Air Conditioner", false));
            appliances.add(new Appliance("Television", false));
        }

        // Background scheduler thread
        Thread scheduler = new Thread(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                try {
                    Calendar now = Calendar.getInstance();
                    int hour = now.get(Calendar.HOUR_OF_DAY);
                    int minute = now.get(Calendar.MINUTE);

                    // Example rule: turn Light ON at 7 PM
                    if (hour == 19 && minute == 0) {
                        for (Appliance app : appliances) {
                            if (app.getName().equalsIgnoreCase("Light") && !app.isOn()) {
                                app.turnOn();
                                saveAppliances(appliances);
                            }
                        }
                    }
                    Thread.sleep(60000); // check every minute
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });


        scheduler.setDaemon(true);
        scheduler.start();

        int choice = -1;
        try (Scanner sc = new Scanner(System.in)) {
            do {
                System.out.println("\n=== Home Appliance Automation System ===");
                System.out.println("1. View All Appliances");
                System.out.println("2. Turn ON an Appliance");
                System.out.println("3. Turn OFF an Appliance");
                System.out.println("4. Add New Appliance");
                System.out.println("5. Exit");
                System.out.print("Enter choice: ");
                try {
                    choice = sc.nextInt();
                } catch (InputMismatchException e) {
                    System.out.println("Invalid input! Please enter a number.");
                    sc.nextLine(); // consume invalid input
                    continue;
                }

                switch (choice) {
                    case 1:
                        for (int i = 0; i < appliances.size(); i++) {
                            System.out.print((i + 1) + ". ");
                            appliances.get(i).showStatus();
                        }
                        break;

                    case 2:
                        System.out.print("Enter appliance number to turn ON: ");
                        int onChoice = sc.nextInt();
                        sc.nextLine(); // consume newline
                        if (onChoice >= 1 && onChoice <= appliances.size()) {
                            appliances.get(onChoice - 1).turnOn();
                            saveAppliances(appliances);
                        } else {
                            System.out.println("Invalid choice!");
                        }
                        break;

                    case 3:
                        System.out.print("Enter appliance number to turn OFF: ");
                        int offChoice = sc.nextInt();
                        sc.nextLine(); // consume newline
                        if (offChoice >= 1 && offChoice <= appliances.size()) {
                            appliances.get(offChoice - 1).turnOff();
                            saveAppliances(appliances);
                        } else {
                            System.out.println("Invalid choice!");
                        }
                        break;

                    case 4:
                        sc.nextLine(); // consume newline
                        System.out.print("Enter new appliance name: ");
                        String newApp = sc.nextLine();
                        appliances.add(new Appliance(newApp, false));
                        saveAppliances(appliances);
                        System.out.println(newApp + " added successfully!");
                        break;

                    case 5:
                        saveAppliances(appliances);
                        System.out.println("Exiting... Thank you!");
                        scheduler.interrupt();
                        break;

                    default:
                        System.out.println("Invalid choice!");
                }

            } while (choice != 5);
        }
    }

    public static void saveAppliances(List<Appliance> appliances) {
        File dir = new File("data");
        if (!dir.exists()) {
            dir.mkdirs();
        }
        try (PrintWriter writer = new PrintWriter(new FileWriter(FILE_NAME))) {
            for (Appliance app : appliances) {
                writer.println(app.getStatusString());
            }
        } catch (IOException e) {
            System.out.println("Error saving appliances: " + e.getMessage());
        }
    }

    private static List<Appliance> loadAppliances() {
        List<Appliance> appliances = new ArrayList<>();
        File file = new File(FILE_NAME);
        if (file.exists()) {
            try (BufferedReader reader = new BufferedReader(new FileReader(FILE_NAME))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    appliances.add(Appliance.fromString(line));
                }
            } catch (IOException e) {
                System.out.println("Error loading appliances: " + e.getMessage());
            }
        }
        return appliances;
    }
}

