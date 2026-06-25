package com.example.backend.controllers;

import com.example.backend.services.AuthService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "*")
public class AuthController {

    @Autowired
    private AuthService authService;

    @PostMapping("/register")
    public ResponseEntity<Map<String, Object>> register(@RequestBody Map<String, String> body) {
        try {
            String fullName = body.get("fullName");
            String email = body.get("email");
            String password = body.get("password");
            String aadharNumber = body.get("aadharNumber");

            if (fullName == null || email == null || password == null || aadharNumber == null) {
                return ResponseEntity.badRequest().body(Map.of("success", false, "message", "All fields are required."));
            }

            Map<String, Object> result = authService.register(fullName, email, password, aadharNumber);
            boolean success = (boolean) result.get("success");
            return success ? ResponseEntity.ok(result) : ResponseEntity.badRequest().body(result);

        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("success", false, "message", "Server error: " + e.getMessage()));
        }
    }

    @PostMapping("/login")
    public ResponseEntity<Map<String, Object>> login(@RequestBody Map<String, String> body) {
        try {
            String email = body.get("email");
            String password = body.get("password");

            if (email == null || password == null) {
                return ResponseEntity.badRequest().body(Map.of("success", false, "message", "Email and password are required."));
            }

            Map<String, Object> result = authService.login(email, password);
            boolean success = (boolean) result.get("success");
            return success ? ResponseEntity.ok(result) : ResponseEntity.status(401).body(result);

        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("success", false, "message", "Server error: " + e.getMessage()));
        }
    }
}
