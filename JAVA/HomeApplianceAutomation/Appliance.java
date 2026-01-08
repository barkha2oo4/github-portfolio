import java.io.Serializable;

public class Appliance implements Serializable {
    private String name;
    private boolean isOn;

    public Appliance(String name, boolean isOn) {
        this.name = name;
        this.isOn = isOn;
    }

    public String getName() {
        return name;
    }

    public boolean isOn() {
        return isOn;
    }

    public void turnOn() {
        isOn = true;
        System.out.println(name + " is now ON.");
    }

    public void turnOff() {
        isOn = false;
        System.out.println(name + " is now OFF.");
    }

    public String getStatusString() {
        return name + "," + isOn;
    }

    public static Appliance fromString(String line) {
        String[] parts = line.split(",");
        if (parts.length != 2) {
            throw new IllegalArgumentException("Invalid appliance string: " + line);
        }
        String name = parts[0];
        boolean isOn = false;
        if (parts[1].equalsIgnoreCase("true") || parts[1].equalsIgnoreCase("on")) {
            isOn = true;
        }
        return new Appliance(name, isOn);
    }

    public void showStatus() {
        System.out.println(name + " Status: " + (isOn ? "ON" : "OFF"));
    }
}
