package com.example.backend.repositories;

import com.example.backend.models.Application;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
public class ApplicationRepository {

    private final List<Application> applications = new ArrayList<>();

    public Application save(Application application) {
        if (application.getId() == null || application.getId().isEmpty()) {
            application.setId(UUID.randomUUID().toString());
        }
        if (application.getStatus() == null) {
            application.setStatus("PENDING");
        }
        if (application.getSubmittedAt() == null) {
            application.setSubmittedAt(Instant.now().toString());
        }

        applications.add(application);
        System.out.println("Saved application to in-memory store. Total applications: " + applications.size());
        return application;
    }

    public List<Application> findAll() {
        return new ArrayList<>(applications);
    }
}
