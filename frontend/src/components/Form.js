import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import DonutLargeIcon from '@mui/icons-material/DonutLarge';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme();

export default function Form({applyInputs}) {
  const [amplitude, setAmplitude] = React.useState(10)
  const [frequence, setFrequence] = React.useState(10)
  const [temps, setTemps] = React.useState(10)

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!amplitude) return;
    if (!frequence) return;
    if (!temps) return;
    console.log(typeof(amplitude))
    console.log(typeof(frequence))
    console.log(typeof(temps))
    if (temps<0) {
      alert('time should be positive')
      return 
    };
    if (frequence<0) {
      alert('frequency should be positive')
      return 
    };

    // if (!(typeof(amplitude)==='number')) return;
    // if (!(typeof(frequence)==='number')) return;
    // if (!(typeof(temps)==='number')) return;

    const newInputs = {
      amplitude: amplitude,
      frequence: frequence,
      temps: temps,
    }

    applyInputs(newInputs)
  };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <DonutLargeIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
              Sinusoïde
          </Typography>
          <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  autoComplete="given-name"
                  name="amplitude"
                  required
                  fullWidth
                  id="amplitude"
                  label="Amplitude"
                  autoFocus
                  value={amplitude}
                  onChange={e => setAmplitude(e.target.value)}
                  type='number'
              />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  id="frequence"
                  label="Fréquence"
                  name="frequence"
                  autoComplete="Fréquence"
                  value={frequence}
                  onChange={e => setFrequence(e.target.value)}
                  type='number'
              />
              </Grid>
              <Grid item xs={12} sm={12}>
                <TextField
                  required
                  fullWidth
                  id="temps"
                  label="Temps"
                  name="temps"
                  autoComplete="Temps"
                  value={temps}
                  onChange={e => setTemps(e.target.value)}
                  type='number'
              />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Afficher
            </Button>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}