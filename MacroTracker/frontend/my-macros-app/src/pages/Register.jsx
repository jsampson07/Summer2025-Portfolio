import { useState, useContext } from "react";
import API from "../api/axios";
import AuthContext from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const [form, setForm] = useState({
    username: "",
    password: "",
    email: "",
    age: "",
    weight: "",
    goal: "casual",
  });

  const { login } = useContext(AuthContext);
  const navigate = useNavigate();
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await API.post("/register", {
        username: form.username,
        password: form.password,
        email: form.email,
        age: form.age ? parseInt(form.age) : null,
        weight: form.weight ? parseFloat(form.weight) : null,
        goal: form.goal || null,
      });

      // ✅ success — login and redirect to homepage
      const tokenRes = await API.post("/login", {
        username: form.username,
        password: form.password,
      });
      login(tokenRes.data.access_token);
      navigate("/");
    } catch (err) {
        if (err.response?.data?.error_message) {
            const msg = err.response.data.error_message;

            if (Array.isArray(msg)) {
                // Comes from Pydantic validation — show field-specific messages
                const combined = msg.map((e) => `${e.loc[0]}: ${e.msg}`).join(", ");
                setError(combined);
            } else if (typeof msg === "string") {
                setError(msg);
            } else {
                setError("Something went wrong.");
            }
        } else {
            setError("Registration failed. No response from server.");
        }
    }
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      <h2>Register</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <input
        type="text"
        name="username"
        placeholder="Username"
        value={form.username}
        onChange={handleChange}
        required
      />
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={form.email}
        onChange={handleChange}
        required
      />
      <input
        type="password"
        name="password"
        placeholder="Password"
        value={form.password}
        onChange={handleChange}
        required
      />
      <input
        type="number"
        name="age"
        placeholder="Age (optional)"
        value={form.age}
        onChange={handleChange}
      />
      <input
        type="number"
        name="weight"
        placeholder="Weight (optional)"
        value={form.weight}
        onChange={handleChange}
      />
      <select name="goal" value={form.goal} onChange={handleChange}>
        <option value="casual">Casual</option>
        <option value="bulk">Bulk</option>
        <option value="cut">Cut</option>
        <option value="maintain">Maintain</option>
      </select>
      <button type="submit">Create Account</button>
    </form>
  );
}