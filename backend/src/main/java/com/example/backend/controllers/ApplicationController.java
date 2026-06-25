package com.example.backend.controllers;

import com.example.backend.models.Application;
import com.example.backend.services.ApplicationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/applications")
@CrossOrigin(origins = "*") // Allows Flutter web/emulator to call this API
public class ApplicationController {

    @Autowired
    private ApplicationService applicationService;

    @PostMapping
    public ResponseEntity<?> submitApplication(@RequestBody Application application) {
        try {
            Application saved = applicationService.submitApplication(application);
            return ResponseEntity.ok(saved);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body("Error submitting application: " + e.getMessage());
        }
    }
}
