package com.example.backend.controllers;

import com.example.backend.models.Subsidy;
import com.example.backend.services.SubsidyService;
import com.example.backend.services.SchemeUpdateService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/subsidies")
@CrossOrigin(origins = "*")
public class SubsidyController {

    @Autowired
    private SubsidyService subsidyService;

    @Autowired
    private SchemeUpdateService schemeUpdateService;

    // Fetch all active schemes
    @GetMapping
    public ResponseEntity<List<Subsidy>> getAllSubsidies(
            @RequestParam(name = "state", required = false) String state,
            @RequestParam(name = "category", required = false) String category,
            @RequestParam(name = "search", required = false) String search,
            @RequestParam(name = "limit", defaultValue = "20") int limit) throws Exception {
        
        List<Subsidy> subsidies = subsidyService.getSubsidies(state, category, search, limit);
        return ResponseEntity.ok(subsidies);
    }

    // DYNAMIC SYNC: Trigger fetching schemes from remote sources
    @PostMapping("/sync")
    public ResponseEntity<Map<String, Object>> syncSchemes() {
        Map<String, Object> result = schemeUpdateService.syncFromAllSources();
        return ResponseEntity.ok(result);
    }

    // Admin API: Add a newly scraped or manually entered scheme
    @PostMapping
    public ResponseEntity<Subsidy> createSubsidy(@RequestBody Subsidy subsidy) throws Exception {
        Subsidy savedSubsidy = subsidyService.saveSubsidy(subsidy);
        return ResponseEntity.ok(savedSubsidy);
    }

    // Admin API: Update or deactivate an existing scheme
    @PutMapping("/{id}")
    public ResponseEntity<Subsidy> updateSubsidy(@PathVariable String id, @RequestBody Subsidy subsidy) {
        try {
            Subsidy updatedSubsidy = subsidyService.updateSubsidy(id, subsidy);
            return ResponseEntity.ok(updatedSubsidy);
        } catch (Exception e) {
            return ResponseEntity.notFound().build();
        }
    }
}
