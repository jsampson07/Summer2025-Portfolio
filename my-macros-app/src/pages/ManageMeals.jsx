import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";

const styles = {
  container: { maxWidth: 800, margin: "2rem auto", fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif" },
  header: { textAlign: "center", marginBottom: "1.5rem", color: "#333" },
  button: {
    padding: "0.5rem 1rem",
    margin: "0.3rem",
    border: "none",
    borderRadius: 4,
    cursor: "pointer",
    backgroundColor: "#007bff",
    color: "white",
    fontWeight: "600",
    transition: "background-color 0.3s",
  },
  buttonHover: { backgroundColor: "#0056b3" },
  cancelButton: { backgroundColor: "#6c757d" },
  mealList: { listStyle: "none", padding: 0 },
  mealItem: {
    backgroundColor: "white",
    borderRadius: 8,
    padding: "1rem",
    marginBottom: "1rem",
    boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    flexWrap: "wrap",
  },
  mealName: { fontWeight: "700", fontSize: "1.2rem", color: "#222" },
  savedHeart: { color: "red", marginLeft: 6 },
  controlsGroup: { display: "flex", gap: "0.5rem", flexWrap: "wrap", marginTop: 8 },
  formCard: {
    backgroundColor: "#f9f9f9",
    padding: "1.5rem",
    borderRadius: 8,
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
    marginBottom: "2rem",
  },
  formRow: { display: "flex", gap: "1rem", flexWrap: "wrap", marginBottom: "1rem" },
  input: {
    padding: "0.5rem",
    fontSize: "1rem",
    borderRadius: 4,
    border: "1px solid #ccc",
    flexGrow: 1,
    minWidth: 120,
  },
  select: {
    padding: "0.5rem",
    fontSize: "1rem",
    borderRadius: 4,
    border: "1px solid #ccc",
    minWidth: 180,
  },
  foodList: { marginTop: 8, maxHeight: 140, overflowY: "auto", paddingLeft: 0 },
  foodListItem: {
    listStyle: "none",
    padding: "0.3rem 0",
    borderBottom: "1px solid #ddd",
    display: "flex",
    justifyContent: "space-between",
  },
  error: { color: "crimson", fontWeight: "600", marginBottom: "1rem" },

  // New styles for aligned labels + asterisk
  label: {
    display: "flex",
    flexDirection: "column",
    flexGrow: 1,
    minWidth: 140,
    marginBottom: "0.75rem",
    color: "#333",
    fontWeight: "600",
  },
  labelText: {
    display: "flex",
    alignItems: "center",
    gap: 4,
    fontWeight: "600",
    color: "#333",
    marginBottom: 4,
  },
  required: {
    color: "red",
    fontWeight: "700",
  },
};

export default function ManageMeals() {
  const { token } = useAuth();
  const [meals, setMeals] = useState([]);
  const [foods, setFoods] = useState([]);

  const [newMealName, setNewMealName] = useState("");
  const [selectedMealId, setSelectedMealId] = useState(null);
  const [selectedMealFoods, setSelectedMealFoods] = useState([]);
  const [foodToAdd, setFoodToAdd] = useState({ name: "", quantity: 1 });
  const [showMealForm, setShowMealForm] = useState(false);
  const [mealFormFoods, setMealFormFoods] = useState([]);
  const [error, setError] = useState("");

  const [successMessage, setSuccessMessage] = useState("");

  // New food form state
  const [newFood, setNewFood] = useState({
    name: "",
    calories: "",
    protein: "",
    carbs: "",
    fat: "",
    serving_size: "",
    serving_unit: "",
  });

  useEffect(() => {
    if (token) {
      fetchMeals();
      fetchFoods();
    }
  }, [token]);

  const fetchMeals = async () => {
    try {
      const res = await fetch("http://localhost:5000/api/meals", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setMeals(data);
    } catch (err) {
      setError("Failed to fetch meals.");
      console.error(err);
    }
  };

  const fetchFoods = async () => {
    try {
      const res = await fetch("http://localhost:5000/api/foods", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setFoods(data);
    } catch (err) {
      setError("Failed to fetch foods.");
      console.error(err);
    }
  };

  // Block letters and invalid keys on integer inputs
  const blockInvalidKeysInteger = (e) => {
    if (
      !(
        (e.key >= "0" && e.key <= "9") ||
        e.key === "Backspace" ||
        e.key === "Delete" ||
        e.key === "ArrowLeft" ||
        e.key === "ArrowRight" ||
        e.key === "Tab"
      )
    ) {
      e.preventDefault();
    }
  };

  // Block invalid keys on decimal inputs (allow only one dot)
  const blockInvalidKeysDecimal = (e) => {
    const val = e.currentTarget.value;
    if (
      !(
        (e.key >= "0" && e.key <= "9") ||
        e.key === "." ||
        e.key === "Backspace" ||
        e.key === "Delete" ||
        e.key === "ArrowLeft" ||
        e.key === "ArrowRight" ||
        e.key === "Tab"
      )
    ) {
      e.preventDefault();
    } else if (e.key === "." && val.includes(".")) {
      e.preventDefault();
    }
  };

  // Sanitize integer inputs
  const handleIntegerInput = (field, value) => {
    const sanitized = value.replace(/[^0-9]/g, "");
    setNewFood((prev) => ({ ...prev, [field]: sanitized }));
  };

  // Sanitize decimal inputs (one dot allowed)
  const handleDecimalInput = (field, value) => {
    let sanitized = value.replace(/[^0-9.]/g, "");
    const parts = sanitized.split(".");
    if (parts.length > 2) {
      sanitized = parts.shift() + "." + parts.join("");
    }
    setNewFood((prev) => ({ ...prev, [field]: sanitized }));
  };

  const createFood = async () => {
    setError("");
    if (!newFood.name.trim()) {
      setError("Food name cannot be empty.");
      return;
    }
    if (!newFood.calories.toString().trim()) {
      setError("Calories is required.");
      return;
    }
    if (!newFood.serving_size.toString().trim()) {
      setError("Serving size is required.");
      return;
    }
    if (!newFood.serving_unit) {
      setError("Serving unit is required.");
      return;
    }
    try {
      const res = await fetch("http://localhost:5000/api/foods", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name: newFood.name,
          calories: parseInt(newFood.calories) || 0,
          protein: parseInt(newFood.protein) || 0,
          carbs: parseInt(newFood.carbs) || 0,
          fat: parseInt(newFood.fat) || 0,
          serving_size: parseFloat(newFood.serving_size) || 1,
          serving_unit: newFood.serving_unit || "unit",
        }),
      });
      if (!res.ok) {
        const errorResp = await res.json();
        if (res.status === 409 && errorResp.error_message) {
          setError(errorResp.error_message);
        } else {
          setError("Failed to create food");
        }
        return;
      }
      const created = await res.json();
      setFoods((prev) => [...prev, created]);
      setNewFood({
        name: "",
        calories: "",
        protein: "",
        carbs: "",
        fat: "",
        serving_size: "",
        serving_unit: "",
      });

      setSuccessMessage(`Food "${created.name}" added successfully!`);
      setTimeout(() => setSuccessMessage(""), 3000);

    } catch (err) {
      setError(err.message);
    }
  };

  const createMeal = async () => {
    setError("");
    if (!newMealName.trim()) {
      setError("Meal name cannot be empty.");
      return;
    }
    if (mealFormFoods.length === 0) {
      setError("Please add at least one food to the meal.");
      return;
    }
    try {
      const foodItemsWithIds = [];
      for (const item of mealFormFoods) {
        let food = foods.find((f) => f.name === item.name);
        if (!food) continue;
        foodItemsWithIds.push({
          food_id: food.id,
          quantity: item.quantity,
        });
      }
      const res = await fetch("http://localhost:5000/api/meals", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name: newMealName,
          saved: false,
          food_items: foodItemsWithIds,
        }),
      });
      if (!res.ok) throw new Error("Failed to create meal");
      const createdMeal = await res.json();
      setMeals((prevMeals) => [...prevMeals, createdMeal]);
      setNewMealName("");
      setMealFormFoods([]);
      setShowMealForm(false);
    } catch (err) {
      setError(err.message);
    }
  };

  const addFoodToForm = () => {
    setError("");
    if (!foodToAdd.name || !foodToAdd.quantity) {
      setError("Please select a food and specify quantity.");
      return;
    }
    if (mealFormFoods.some((item) => item.name === foodToAdd.name)) {
      setError("This food has already been added to the meal!");
      return;
    }
    setMealFormFoods((prev) => [...prev, foodToAdd]);
    setFoodToAdd({ name: "", quantity: 1 });
  };

  const handleSelectMeal = async (id) => {
    setSelectedMealId(id);
    try {
      const res = await fetch(`http://localhost:5000/api/meals/${id}/foods`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setSelectedMealFoods(data);
    } catch (err) {
      setError("Failed to fetch meal foods.");
    }
  };

  const deleteMeal = async (id) => {
    try {
      await fetch(`http://localhost:5000/api/meals/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      setMeals((prev) => prev.filter((meal) => meal.id !== id));
      if (selectedMealId === id) {
        setSelectedMealId(null);
        setSelectedMealFoods([]);
      }
    } catch (err) {
      setError("Failed to delete meal.");
    }
  };

  const updateMeal = async (id, updates) => {
    try {
      const res = await fetch(`http://localhost:5000/api/meals/${id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(updates),
      });
      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.error_message || "Failed to update meal");
      }
      const updatedMeal = await res.json();
      setMeals((prevMeals) =>
        prevMeals.map((meal) =>
          meal.id === id ? { ...meal, ...updatedMeal } : meal
        )
      );
    } catch (err) {
      setError("Failed to update meal.");
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Manage Meals</h1>
      {error && <p style={styles.error}>{error}</p>}

      {successMessage && (
        <p style={{ color: "green", fontWeight: "600", marginBottom: "1rem" }}>
          {successMessage}
        </p>
      )}

      {/* Add Food Section */}
      <div style={styles.formCard}>
        <h2>Add New Food</h2>
        <div style={styles.formRow}>
          <label style={styles.label}>
            <div style={styles.labelText}>
              Name<span style={styles.required}>*</span>
            </div>
            <input
              placeholder="Name"
              value={newFood.name}
              onChange={(e) => setNewFood({ ...newFood, name: e.target.value })}
              style={styles.input}
            />
          </label>
          <label style={styles.label}>
            <div style={styles.labelText}>
              Calories<span style={styles.required}>*</span>
            </div>
            <input
              placeholder="Calories"
              type="text"
              inputMode="numeric"
              value={newFood.calories}
              onKeyDown={blockInvalidKeysInteger}
              onChange={(e) => handleIntegerInput("calories", e.target.value)}
              style={styles.input}
            />
          </label>
          <label style={styles.label}>
            <div style={styles.labelText}>Protein</div>
            <input
              placeholder="Protein"
              type="text"
              inputMode="numeric"
              value={newFood.protein}
              onKeyDown={blockInvalidKeysInteger}
              onChange={(e) => handleIntegerInput("protein", e.target.value)}
              style={styles.input}
            />
          </label>
          <label style={styles.label}>
            <div style={styles.labelText}>Carbs</div>
            <input
              placeholder="Carbs"
              type="text"
              inputMode="numeric"
              value={newFood.carbs}
              onKeyDown={blockInvalidKeysInteger}
              onChange={(e) => handleIntegerInput("carbs", e.target.value)}
              style={styles.input}
            />
          </label>
          <label style={styles.label}>
            <div style={styles.labelText}>Fat</div>
            <input
              placeholder="Fat"
              type="text"
              inputMode="numeric"
              value={newFood.fat}
              onKeyDown={blockInvalidKeysInteger}
              onChange={(e) => handleIntegerInput("fat", e.target.value)}
              style={styles.input}
            />
          </label>
          <label style={styles.label}>
            <div style={styles.labelText}>
              Serving Size<span style={styles.required}>*</span>
            </div>
            <input
              placeholder="Serving Size"
              type="text"
              inputMode="decimal"
              value={newFood.serving_size}
              onKeyDown={blockInvalidKeysDecimal}
              onChange={(e) => handleDecimalInput("serving_size", e.target.value)}
              style={styles.input}
            />
          </label>
          <label style={styles.label}>
            <div style={styles.labelText}>
              Serving Unit<span style={styles.required}>*</span>
            </div>
            <select
              value={newFood.serving_unit}
              onChange={(e) => setNewFood({ ...newFood, serving_unit: e.target.value })}
              style={styles.select}
            >
              <option value="">Select unit</option>
              <option value="g">grams (g)</option>
              <option value="oz">ounces (oz)</option>
              <option value="ml">milliliter (mL)</option>
              <option value="cup">cups (c)</option>
              <option value="unit">unit (u)</option>
            </select>
          </label>
        </div>
        <button
          style={{
            ...styles.button,
            opacity:
              !newFood.name.trim() ||
              !newFood.calories.toString().trim() ||
              !newFood.serving_size.toString().trim() ||
              !newFood.serving_unit
                ? 0.5
                : 1,
            cursor:
              !newFood.name.trim() ||
              !newFood.calories.toString().trim() ||
              !newFood.serving_size.toString().trim() ||
              !newFood.serving_unit
                ? "not-allowed"
                : "pointer",
          }}
          disabled={
            !newFood.name.trim() ||
            !newFood.calories.toString().trim() ||
            !newFood.serving_size.toString().trim() ||
            !newFood.serving_unit
          }
          onClick={createFood}
        >
          Add Food
        </button>
      </div>

      {/* Add Meal Button */}
      <button
        style={styles.button}
        onClick={() => setShowMealForm(true)}
        onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#0056b3")}
        onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "#007bff")}
      >
        Add Meal
      </button>

      {showMealForm && (
        <div style={styles.formCard}>
          <h2>Create New Meal</h2>
          <input
            placeholder="Meal Name"
            value={newMealName}
            onChange={(e) => setNewMealName(e.target.value)}
            style={styles.input}
          />
          <div style={styles.formRow}>
            <select
              value={foodToAdd.name}
              onChange={(e) => setFoodToAdd({ ...foodToAdd, name: e.target.value })}
              style={styles.select}
            >
              <option value="">Select a food</option>
              {foods.map((food) => (
                <option key={food.id} value={food.name}>
                  {food.name}
                </option>
              ))}
            </select>
            <input
              type="number"
              placeholder="Quantity"
              value={foodToAdd.quantity}
              min="0.1"
              step="0.1"
              onChange={(e) =>
                setFoodToAdd({ ...foodToAdd, quantity: parseFloat(e.target.value) })
              }
              style={{ ...styles.input, maxWidth: 120 }}
            />
            <button style={styles.button} onClick={addFoodToForm}>
              Add Food to Meal
            </button>
          </div>
          <ul style={styles.foodList}>
            {mealFormFoods.map((item, idx) => (
              <li key={idx} style={styles.foodListItem}>
                {item.name} — Quantity: {item.quantity}
              </li>
            ))}
          </ul>
          <div style={{ marginTop: "1rem" }}>
            <button style={styles.button} onClick={createMeal}>
              Submit Meal
            </button>
            <button
              style={{ ...styles.button, ...styles.cancelButton, marginLeft: "1rem" }}
              onClick={() => setShowMealForm(false)}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {meals.length === 0 ? (
        <p>No meals found.</p>
      ) : (
        <ul style={styles.mealList}>
          {meals.map((meal) => (
            <li key={meal.id} style={styles.mealItem}>
              <span style={styles.mealName}>
                {meal.name} {meal.saved && <span style={styles.savedHeart}>❤️</span>}
              </span>
              <div style={styles.controlsGroup}>
                <button style={styles.button} onClick={() => handleSelectMeal(meal.id)}>
                  View
                </button>
                <button
                  style={{ ...styles.button, ...styles.cancelButton }}
                  onClick={() => deleteMeal(meal.id)}
                >
                  Delete
                </button>
                <button
                  style={styles.button}
                  onClick={() =>
                    updateMeal(meal.id, { name: prompt("Rename meal:", meal.name) || meal.name })
                  }
                >
                  Rename
                </button>
                <button
                  style={styles.button}
                  onClick={() => updateMeal(meal.id, { name: meal.name, saved: !meal.saved })}
                >
                  {meal.saved ? "Unfavorite" : "Favorite"}
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}

      {selectedMealId && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Foods in Selected Meal</h2>
          {selectedMealFoods.length === 0 ? (
            <p>No foods found in this meal.</p>
          ) : (
            <ul>
              {selectedMealFoods.map((food) => (
                <li key={food.id}>
                  {food.name} - Quantity: {food.quantity}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}