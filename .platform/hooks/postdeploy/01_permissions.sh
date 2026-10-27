#!/bin/bash
mkdir -p /var/app/current/data/papers /var/app/current/data/extracted_texts /var/app/current/data/database /var/app/current/Downloaded_pdfs /tmp/litwise_papers
chown -R webapp:webapp /var/app/current/data /var/app/current/Downloaded_pdfs /tmp/litwise_papers 2>/dev/null || true
chmod -R 777 /var/app/current/data /var/app/current/Downloaded_pdfs /tmp/litwise_papers 2>/dev/null || true
