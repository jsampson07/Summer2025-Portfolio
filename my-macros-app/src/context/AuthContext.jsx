import { createContext, useContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const navigate = useNavigate();

  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [userId, setUserId] = useState(() =>
    token ? jwtDecode(token).sub || jwtDecode(token).identity : null
  );

  const login = (newToken) => {
    setToken(newToken);
    localStorage.setItem("token", newToken);
    setUserId(jwtDecode(newToken).sub || jwtDecode(newToken).identity);
  };

  const logout = () => {
    setToken(null);
    setUserId(null);
    localStorage.removeItem("token");
    navigate("/login"); // redirect after logout
  };

  return (
    <AuthContext.Provider value={{ token, userId, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;