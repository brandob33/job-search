// Usage: node coverletter.js spec.json out.docx
// spec: { date, company, role, location?, greeting?, paragraphs: [str...] }
const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, AlignmentType, BorderStyle } = require('docx');
const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const F = 'Calibri';
const run = (t, o = {}) => new TextRun({ text: t, font: F, size: o.size || 22, bold: o.bold, color: o.color });
const p = (children, o = {}) => new Paragraph({ children, alignment: o.align, spacing: { after: o.after ?? 160, line: 276 }, border: o.border });

const kids = [
  p([run('Brandon Burns', { size: 36, bold: true })], { align: AlignmentType.CENTER, after: 40 }),
  p([run('Irvine, CA | 925.548.9737 | brandontbb33@gmail.com | linkedin.com/in/brandontburns | brandontburns.com', { size: 20 })],
    { align: AlignmentType.CENTER, after: 240, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '999999', space: 6 } } }),
  p([run(spec.date)], { after: 200 }),
  p([run(`Hiring Team, ${spec.company}`)], { after: 0 }),
  p([run(`Re: ${spec.role}${spec.req ? ' (' + spec.req + ')' : ''}`)], { after: 200 }),
  p([run(spec.greeting || `Dear ${spec.company} Hiring Team,`)]),
  ...spec.paragraphs.map(t => p([run(t)])),
  p([run('Sincerely,')], { after: 0 }),
  p([run('Brandon Burns')]),
];
const doc = new Document({
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 } } }, children: kids }],
});
Packer.toBuffer(doc).then(b => fs.writeFileSync(process.argv[3], b));
