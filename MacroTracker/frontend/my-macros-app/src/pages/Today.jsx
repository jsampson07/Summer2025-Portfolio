import { useEffect, useState, useContext } from "react";
import AuthContext from "../context/AuthContext";
import API, { setAuthToken } from "../api/axios";

export default function Today() {
  const { token } = useContext(AuthContext);
  const [meals, setMeals] = useState([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [editingMealId, setEditingMealId] = useState(null);
  const [mealFoods, setMealFoods] = useState({}); // { mealId: [{ food_id, name, quantity }] }

  useEffect(() => {
    fetchMeals();
  }, [token]);

  const fetchMeals = () => {
    if (token) {
      setAuthToken(token);
      API.get("/meals")
        .then((res) => setMeals(res.data))
        .catch(() => setError("Failed to load meals."));
    }
  };

  const fetchMealFoods = async (mealId) => {
    try {
      const res = await API.get(`/meals/${mealId}/foods`);
      setMealFoods((prev) => ({ ...prev, [mealId]: res.data }));
    } catch {
      setError("Failed to load foods for this meal.");
    }
  };

  const handleEditClick = (mealId) => {
    if (editingMealId === mealId) {
      setEditingMealId(null);
    } else {
      fetchMealFoods(mealId);
      setEditingMealId(mealId);
    }
  };

  const handleQuantityChange = (mealId, foodId, value) => {
    if (/^\d*\.?\d*$/.test(value)) {
      setMealFoods((prev) => ({
        ...prev,
        [mealId]: prev[mealId].map((food) =>
          food.food_id === foodId ? { ...food, quantity: value } : food
        ),
      }));
    }
  };

  const saveQuantityChange = async (mealId, foodId, quantity) => {
    try {
      await API.patch(`/meals/${mealId}/foods`, {
        food_id: foodId,
        quantity: parseFloat(quantity) || 0,
      });
      setSuccess("Quantity updated!");
      setTimeout(() => setSuccess(""), 3000);
      fetchMeals();
    } catch {
      setError("Failed to update quantity.");
    }
  };

  const deleteMeal = async (mealId) => {
    try {
      await API.delete(`/meals/${mealId}`);
      setSuccess("Meal deleted.");
      setTimeout(() => setSuccess(""), 3000);
      fetchMeals();
    } catch {
      setError("Failed to delete meal.");
    }
  };

  const dailyTotals = meals.reduce(
    (acc, meal) => {
      acc.calories += meal.total_calories || 0;
      acc.protein += meal.total_protein || 0;
      acc.carbs += meal.total_carbs || 0;
      acc.fat += meal.total_fat || 0;
      return acc;
    },
    { calories: 0, protein: 0, carbs: 0, fat: 0 }
  );

  return (
    <div className="page">
      <h1>Today's Meals</h1>

      {/* Friendly message when no meals */}
      {meals.length === 0 && !error && (
        <div
          style={{
            marginTop: "2rem",
            padding: "1.5rem",
            backgroundColor: "#e0f7fa",
            borderRadius: "12px",
            textAlign: "center",
            color: "#00796b",
            fontWeight: "600",
            fontSize: "1.3rem",
            boxShadow: "0 4px 8px rgba(0, 121, 107, 0.2)",
            userSelect: "none",
            maxWidth: "400px",
            marginLeft: "auto",
            marginRight: "auto",
            lineHeight: "1.4",
          }}
        >
          Let&apos;s get our day started and eat our first meal! 🥗✨
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
      {success && <p style={{ color: "green" }}>{success}</p>}

      <div style={{ display: "grid", gap: "1rem" }}>
        {meals.map((meal) => (
          <div
            key={meal.id}
            style={{
              border: "1px solid #ddd",
              borderRadius: "10px",
              padding: "1rem",
              backgroundColor: "#fff",
              boxShadow: "0 2px 5px rgba(0,0,0,0.05)",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <h3>{meal.name}</h3>
              <div>
                <button onClick={() => handleEditClick(meal.id)}>
                  {editingMealId === meal.id ? "Close" : "Edit"}
                </button>
                <button
                  onClick={() => deleteMeal(meal.id)}
                  style={{ marginLeft: "0.5rem", color: "red" }}
                >
                  Delete
                </button>
              </div>
            </div>
            <p>Calories: {meal.total_calories?.toFixed(1)}</p>
            <p>Protein: {meal.total_protein?.toFixed(1)} g</p>
            <p>Carbs: {meal.total_carbs?.toFixed(1)} g</p>
            <p>Fat: {meal.total_fat?.toFixed(1)} g</p>

            {editingMealId === meal.id && mealFoods[meal.id] && (
              <div style={{ marginTop: "1rem" }}>
                <h4>Edit Foods</h4>
                {mealFoods[meal.id].map((food) => (
                  <div
                    key={food.food_id}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "0.5rem",
                      marginBottom: "0.5rem",
                    }}
                  >
                    <span>{food.name}</span>
                    <input
                      type="text"
                      value={food.quantity}
                      onChange={(e) =>
                        handleQuantityChange(meal.id, food.food_id, e.target.value)
                      }
                      style={{ width: "60px", textAlign: "right" }}
                    />
                    <button
                      onClick={() =>
                        saveQuantityChange(meal.id, food.food_id, food.quantity)
                      }
                    >
                      Save
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      <div
        style={{
          position: "fixed",
          bottom: "1rem",
          right: "1rem",
          backgroundColor: "#f8f8f8",
          padding: "0.75rem 1rem",
          borderRadius: "8px",
          fontSize: "0.9rem",
          boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
        }}
      >
        <h4 style={{ margin: "0 0 0.5rem" }}>Daily Totals</h4>
        <p>Calories: {dailyTotals.calories.toFixed(1)}</p>
        <p>Protein: {dailyTotals.protein.toFixed(1)} g</p>
        <p>Carbs: {dailyTotals.carbs.toFixed(1)} g</p>
        <p>Fat: {dailyTotals.fat.toFixed(1)} g</p>
      </div>
    </div>
  );
}
