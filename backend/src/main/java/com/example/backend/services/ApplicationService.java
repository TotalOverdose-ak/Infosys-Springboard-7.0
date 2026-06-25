package com.example.backend.services;

import com.example.backend.models.Application;
import com.example.backend.repositories.ApplicationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.concurrent.ExecutionException;

@Service
public class ApplicationService {

    @Autowired
    private ApplicationRepository applicationRepository;

    public Application submitApplication(Application application) throws ExecutionException, InterruptedException {
        return applicationRepository.save(application);
    }
}
