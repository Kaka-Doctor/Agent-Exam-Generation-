// Netlify Function: Generate Exam
const EXAM_DATA = require('../../data/question-banks/exam-data.js');

const BK_TOPICS = {
  form1: [
    { id: 'F1T1', title: 'The Concept of Bible and Bible Knowledge' },
    { id: 'F1T2', title: "God's Creation" },
    { id: 'F1T3', title: 'The Fall of Man' },
    { id: 'F1T4', title: 'The Formation of Patriarchs' },
  ],
  form2: [
    { id: 'F2T1', title: "God's Love and Compassion" },
    { id: 'F2T2', title: 'The Sinai Covenant' },
    { id: 'F2T3', title: 'Statistics and Census' },
    { id: 'F2T4', title: 'Leadership' },
    { id: 'F2T5', title: 'Patriotism' },
  ],
};
const DV_TOPICS = {
  form5: [
    { id: 'F5T1', title: 'Introduction to Divinity' },
    { id: 'F5T2', title: 'Governance' },
    { id: 'F5T3', title: 'Courage and Decision-Making' },
    { id: 'F5T4', title: 'The Teachings of Prophet Isaiah' },
    { id: 'F5T5', title: 'Social Justice and Community Rights' },
    { id: 'F5T6', title: 'Compassion, Mercy and Forgiveness' },
    { id: 'F5T7', title: 'Responsibility' },
  ],
  form6: [
    { id: 'F6T1', title: 'Overview of the New Testament Books' },
    { id: 'F6T2', title: 'The Gospel According to Matthew' },
    { id: 'F6T3', title: 'The Gospel According to John' },
    { id: 'F6T4', title: 'The Letter to the Romans' },
    { id: 'F6T5', title: 'The Epistle of James' },
  ],
};

function mulberry32(seed){return function(){seed|=0;seed=seed+0x6D2B79F5|0;let t=seed;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296;};}
function shuffle(a,s){const r=mulberry32(s);const b=[...a];for(let i=b.length-1;i>0;i--){const j=Math.floor(r()*(i+1));[b[i],b[j]]=[b[j],b[i]];}return b;}

function getTopics(lvl,sel){
  if(lvl==='form1')return BK_TOPICS.form1;
  if(lvl==='form2'){const i=BK_TOPICS.form2.findIndex(t=>t.id===sel);return[...BK_TOPICS.form1,...BK_TOPICS.form2.slice(0,i+1)];}
  if(lvl==='form5')return DV_TOPICS.form5;
  if(lvl==='form6'){const i=DV_TOPICS.form6.findIndex(t=>t.id===sel);return[...DV_TOPICS.form5,...DV_TOPICS.form6.slice(0,i+1)];}
  return[];
}

exports.handler=async(e)=>{
  if(e.httpMethod!=='POST')return{statusCode:405,body:JSON.stringify({error:'Method not allowed'})};
  try{
    const b=JSON.parse(e.body||'{}');
    const{level,selectedTopic,examIndex=0,schoolName,examType,examDate}=b;
    const topics=getTopics(level,selectedTopic);
    const idx=parseInt(examIndex)||0;
    const numT=topics.length;
    let exam={topics};

    if(level==='form1'||level==='form2'){
      exam.type='bible-knowledge';
      exam.subjectCode='014';exam.subjectName='BIBLE KNOWLEDGE';exam.duration='2:30 Hours';
      exam.formText=level==='form1'?'FORM ONE':'FORM TWO';

      // Q1: 10 MCQs
      const labels=['(i)','(ii)','(iii)','(iv)','(v)','(vi)','(vii)','(viii)','(ix)','(x)'];
      const perT=Math.floor(10/numT);let rem=10-perT*numT;
      const cnts=Array(numT).fill(perT);for(let i=0;i<rem;i++)cnts[i%numT]++;
      const q1Items=[];let mi=0;
      for(let ti=0;ti<numT;ti++){
        const pool=EXAM_DATA.mcqBank[topics[ti].id]||[];
        const c=cnts[ti];const st=idx*c;
        for(let j=0;j<c;j++){
          const qi=(st+j)%pool.length;const mcq=pool[qi];
          const sh=shuffle(mcq.options,idx*100+mi);
          q1Items.push({label:labels[mi],leadStatement:mcq.lead,options:sh});mi++;
        }
      }
      exam.q1={no:1,stem:'For each of the items (i) – (x), choose the correct answer from the given alternatives and write its letter in the box provided.',items:q1Items};

      // Q2: matching
      const avail=EXAM_DATA.matchingThemes.filter(t=>t.requiredTopics.every(rt=>topics.some(tp=>tp.id===rt)));
      const theme=avail.length>0?avail[idx%avail.length]:EXAM_DATA.matchingThemes[0];
      const sB=shuffle(theme.listB.map(i=>({...i})),idx*7+42);
      sB.forEach((it,i)=>{it.letter=String.fromCharCode(65+i);});
      exam.q2={no:2,stem:theme.stem,listA:theme.listA,listB:sB};

      // Section B: 7 structured questions
      const sB2=[];let qn=3;
      const saPer=Math.floor(7/numT);rem=7-saPer*numT;
      const saCnts=Array(numT).fill(saPer);for(let i=0;i<rem;i++)saCnts[i%numT]++;
      for(let ti=0;ti<numT;ti++){
        const pool=EXAM_DATA.structuredBank[topics[ti].id]||[];
        const c=saCnts[ti];const st=idx*c;
        for(let j=0;j<c&&qn<=9;j++){
          const qi=(st+j)%pool.length;const q=pool[qi];
          sB2.push({...q,no:qn,topic:topics[ti].title});qn++;
        }
      }
      exam.sectionB=sB2;

      // Section C: essay
      const et=topics[idx%numT];
      const ep=EXAM_DATA.essayBank[et.id]||[];
      const ei=idx%ep.length;const es=ep[ei];
      exam.q10={no:10,statement:es.statement,task:es.task,answerLines:40};

    } else {
      exam.type='divinity';
      exam.subjectCode=level==='form5'?'114/1':'114/2';
      exam.subjectName=level==='form5'?'DIVINITY 1':'DIVINITY 2';
      exam.duration='3:00 Hours';
      exam.formText=level==='form5'?'FORM FIVE':'FORM SIX';

      // Section A: 6 questions
      const sa=[];let qn=1;
      if(numT<=6){
        const per=Math.max(1,Math.floor(6/numT));rem=6-per*numT;
        for(let ti=0;ti<numT;ti++){
          const pool=EXAM_DATA.form5SectionA[topics[ti].id]||EXAM_DATA.form6SectionA[topics[ti].id]||[];
          const c=ti<rem?per+1:per;const st=idx*c;
          for(let j=0;j<c&&qn<=6;j++){const qi=(st+j)%pool.length;sa.push({...pool[qi],no:qn++});}
        }
      } else {
        const f5=topics.filter(t=>t.id.startsWith('F5'));const f6=topics.filter(t=>t.id.startsWith('F6'));
        for(let i=0;i<5;i++){
          const t=f5[(idx+i)%f5.length];const pool=EXAM_DATA.form5SectionA[t.id]||[];
          const qi=idx%pool.length;sa.push({...pool[qi],no:qn++});
        }
        if(f6.length>0){const t=f6[idx%f6.length];const pool=EXAM_DATA.form6SectionA[t.id]||[];
          const qi=idx%pool.length;sa.push({...pool[qi],no:qn++});}
      }
      exam.sectionA=sa;

      // Section B: 3 essays
      const sb=[];let en=7;
      if(numT<=3){
        for(const t of topics){
          const pool=EXAM_DATA.form5SectionB[t.id]||EXAM_DATA.form6SectionB[t.id]||[];
          if(pool.length>0){const qi=idx%pool.length;sb.push({...pool[qi],no:en++});}
        }
      } else {
        const f5=topics.filter(t=>t.id.startsWith('F5'));const f6=topics.filter(t=>t.id.startsWith('F6'));
        for(let i=0;i<2;i++){
          const t=f5[(idx+i)%f5.length];const pool=EXAM_DATA.form5SectionB[t.id]||[];
          if(pool.length>0){const qi=idx%pool.length;sb.push({...pool[qi],no:en++});}
        }
        if(f6.length>0){const t=f6[(idx+5)%f6.length];const pool=EXAM_DATA.form6SectionB[t.id]||[];
          if(pool.length>0){const qi=idx%pool.length;sb.push({...pool[qi],no:en++});}}
      }
      exam.sectionB=sb;
    }

    exam.schoolName=schoolName||'TYPE YOUR SCHOOL NAME HERE';
    exam.examType=examType||'TERMINAL/MOCK/PRE-NECTA';
    exam.examDate=examDate||'';

    return{statusCode:200,headers:{'Content-Type':'application/json'},body:JSON.stringify(exam)};
  }catch(err){return{statusCode:500,body:JSON.stringify({error:err.message})};}
};
