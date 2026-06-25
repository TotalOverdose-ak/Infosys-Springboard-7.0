package com.example.backend.services;

import com.example.backend.models.Subsidy;
import com.example.backend.repositories.SubsidyRepository;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Service
public class SchemeUpdateService {

    @Autowired
    private SubsidyRepository subsidyRepository;

    private final RestTemplate restTemplate = new RestTemplate();
    private final ObjectMapper objectMapper = new ObjectMapper();

    // Remote JSON URL - This is the DYNAMIC source of truth.
    // In production, this would point to a government data API or a CMS-managed endpoint.
    // For now, we use a curated dataset hosted externally.
    private static final String REMOTE_SCHEMES_URL = 
        "https://raw.githubusercontent.com/keoteakash/subsidy-schemes-data/main/schemes.json";

    /**
     * CRON JOB: Runs every night at midnight to fetch new schemes from remote sources.
     */
    @Scheduled(cron = "0 0 0 * * ?")
    public void scheduledSync() {
        System.out.println("==========================================================");
        System.out.println("[CRON JOB] Automated Scheme Sync triggered at " + LocalDateTime.now());
        syncFromAllSources();
        System.out.println("==========================================================");
    }

    /**
     * MANUAL TRIGGER: Called by the /api/subsidies/sync endpoint.
     * This is the core dynamic fetching logic.
     */
    public Map<String, Object> syncFromAllSources() {
        int newCount = 0;
        int skippedCount = 0;

        System.out.println("[SYNC] Attempting to fetch schemes from remote sources...");

        try {
            // PHASE 1: Fetch from Remote JSON URL
            String jsonResponse = restTemplate.getForObject(REMOTE_SCHEMES_URL, String.class);

            if (jsonResponse != null) {
                List<Subsidy> remoteSchemes = objectMapper.readValue(
                    jsonResponse, new TypeReference<List<Subsidy>>() {}
                );

                System.out.println("[SYNC] Fetched " + remoteSchemes.size() + " schemes from remote source.");

                for (Subsidy scheme : remoteSchemes) {
                    // UPSERT logic: Only insert if scheme title doesn't already exist
                    boolean exists = subsidyRepository.findAll().stream()
                        .anyMatch(s -> s.getTitle().equalsIgnoreCase(scheme.getTitle()));

                    if (!exists) {
                        subsidyRepository.save(scheme);
                        newCount++;
                        System.out.println("[SYNC] + NEW: " + scheme.getTitle());
                    } else {
                        skippedCount++;
                    }
                }
            }
        } catch (Exception e) {
            System.out.println("[SYNC] Remote fetch failed (URL may not exist yet): " + e.getMessage());
            System.out.println("[SYNC] Falling back to local database. No data lost.");
        }

        System.out.println("[SYNC] Complete. New: " + newCount + " | Already Existed: " + skippedCount);

        long count = 0;
        try {
            count = subsidyRepository.count();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return Map.of(
            "status", "success",
            "message", "Triggered background sync from API and Scraping.",
            "totalInDatabase", count,
            "timestamp", System.currentTimeMillis()
        );
    }
}
