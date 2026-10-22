// Compatibility entry point for the canonical gold asset exporter. No deployment.
const {execFileSync}=require('node:child_process');
const path=require('node:path');
execFileSync('python3',[path.join(__dirname,'build-gold-icons.py')],{stdio:'inherit'});
