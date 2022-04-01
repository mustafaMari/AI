import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.*;

public class FileHandler {
    private final Map<Integer, Vector<Integer>> paths = new HashMap<>();
    private final Map<Integer, Double> weights = new HashMap<>();
    private final Map<Integer, Set<Integer>> allPossiblePaths = new HashMap<>();
    private final Map<Integer, Vector<Double>> routesWithWeights = new HashMap<>();
    private final Map<Integer, Double> pathsCost = new HashMap<>();
    public Double max;
    private int y = 0;

    public FileHandler(String path) {
        try {
            File file = new File(path);
            FileReader fileReader = new FileReader(file);
            BufferedReader bufferedReader = new BufferedReader(fileReader);
            Vector<String> strings = new Vector<>();
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                strings.add(line);
            }
            bufferedReader.close();
            int numberOfNodes = Integer.parseInt(strings.get(0));
            for (int i = 1, x = 0; i <= numberOfNodes; i++, x++) {
                Double weight = Double.valueOf(strings.get(i));
                weights.put(x, weight);
            }
            for (int i = numberOfNodes + 1, x = 0; i < strings.size(); i++, x++) {
                if (strings.get(i).equals("-1")) {
                    paths.put(x, null);
                } else {
                    Vector<Integer> directions = new Vector<>();
                    String[] nodes = strings.get(i).split(" ");
                    for (String node : nodes) {
                        directions.add(Integer.valueOf(node));
                    }
                    paths.put(x, directions);
                }
            }
            setAllPossiblePaths(0, new HashSet<>());
            convertToWeight();
            calculateCostForAllRoutes();
            maxUsingStreamAndLambda(pathsCost);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void setAllPossiblePaths(Integer n, Set<Integer> set) {
        Set<Integer> copy = n != 0 ? new HashSet<>(set) : new HashSet<>();
        for (Integer nextNode : paths.get(n)) {
            if (n == 0)
                set = new HashSet<>();
            set.add(n);
            if (paths.get(nextNode) == null) {
                set.add(nextNode);
                allPossiblePaths.put(y, new HashSet<>(set));
                if (n == 0 || nextNode.equals(paths.get(n).lastElement()))
                    set = new HashSet<>();
                else
                    set = copy;
                y++;
            } else {
                setAllPossiblePaths(nextNode, set);
            }
        }
    }

    private void convertToWeight() {
        for (Map.Entry<Integer, Set<Integer>> entry : allPossiblePaths.entrySet()) {
            Vector<Double> weightsV = new Vector<>();
            for (Integer key : entry.getValue()) {
                weightsV.add(weights.get(key));
            }
            routesWithWeights.put(entry.getKey(), weightsV);
        }
    }

    private void calculateCostForAllRoutes(){
        for (Map.Entry<Integer, Vector<Double>> entry: routesWithWeights.entrySet()){
            pathsCost.put(entry.getKey(), calculateCost(entry.getValue()));
        }
    }

    private double calculateCost(Vector<Double> values) {
        double totalSum = 0;
        for (double v : values) {
            totalSum += v;
        }
        return totalSum + (totalSum/values.size());
    }

    private void maxUsingStreamAndLambda(Map<Integer, Double> map) {
        Optional<Map.Entry<Integer, Double>> maxEntry = map.entrySet()
                .stream()
                .max(Map.Entry.comparingByValue()
                );

        assert maxEntry.orElse(null) != null;
        max = maxEntry.orElse(null).getValue();
    }

    public Double getMax() {
        return max;
    }
}
