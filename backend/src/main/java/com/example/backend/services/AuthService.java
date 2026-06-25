package com.example.backend.services;

import com.example.backend.models.User;
import com.example.backend.models.Role;
import com.example.backend.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.Optional;

@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    public Map<String, Object> register(String fullName, String email, String password, String aadharNumber) throws Exception {
        // Check if email already exists
        if (userRepository.existsByEmail(email)) {
            return Map.of("success", false, "message", "Email already registered!");
        }

        // Check if Aadhar already exists
        if (userRepository.existsByAadharNumber(aadharNumber)) {
            return Map.of("success", false, "message", "Aadhar number already registered!");
        }

        // Create new user
        User user = new User();
        user.setFullName(fullName);
        user.setEmail(email);
        user.setPassword(password); // In production, hash this!
        user.setAadharNumber(aadharNumber);
        user.setRole(Role.ROLE_CITIZEN);
        user.setCreatedAt(java.time.LocalDateTime.now().toString());

        userRepository.save(user);

        return Map.of(
            "success", true,
            "message", "Registration successful!",
            "user", Map.of(
                "id", user.getId(),
                "fullName", user.getFullName(),
                "email", user.getEmail(),
                "role", user.getRole().name()
            )
        );
    }

    public Map<String, Object> login(String email, String password) throws Exception {
        Optional<User> userOpt = userRepository.findByEmail(email);

        if (userOpt.isEmpty()) {
            return Map.of("success", false, "message", "No account found with this email.");
        }

        User user = userOpt.get();

        if (!user.getPassword().equals(password)) {
            return Map.of("success", false, "message", "Incorrect password.");
        }

        return Map.of(
            "success", true,
            "message", "Login successful!",
            "user", Map.of(
                "id", user.getId(),
                "fullName", user.getFullName(),
                "email", user.getEmail(),
                "aadharNumber", user.getAadharNumber(),
                "role", user.getRole().name()
            )
        );
    }
}
